from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.database.connection import get_db
from app.database.models import Occupancy, Hostel, User
from app.schemas.schemas import OccupancyCreate, OccupancyResponse
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/api/occupancy", tags=["Occupancy"])

@router.get("", response_model=List[OccupancyResponse])
def get_occupancy_records(
    hostel_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    limit: int = Query(100, le=500),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Occupancy, Hostel.name, Hostel.block).join(Hostel, Occupancy.hostel_id == Hostel.id)

    if current_user.role == "warden" and current_user.assigned_hostel_id:
        query = query.filter(Occupancy.hostel_id == current_user.assigned_hostel_id)
    elif hostel_id:
        query = query.filter(Occupancy.hostel_id == hostel_id)

    if start_date:
        query = query.filter(Occupancy.date >= start_date)
    if end_date:
        query = query.filter(Occupancy.date <= end_date)

    records = query.order_by(Occupancy.date.desc()).limit(limit).all()

    results = []
    for r in records:
        results.append(OccupancyResponse(
            id=r.Occupancy.id,
            hostel_id=r.Occupancy.hostel_id,
            hostel_name=r.name,
            hostel_block=r.block,
            date=r.Occupancy.date,
            student_count=r.Occupancy.student_count,
            occupancy_percentage=r.Occupancy.occupancy_percentage
        ))
    return results

@router.post("", response_model=OccupancyResponse)
def log_occupancy(payload: OccupancyCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    hostel = db.query(Hostel).filter(Hostel.id == payload.hostel_id).first()
    if not hostel:
        raise HTTPException(status_code=404, detail="Hostel not found")

    occ_pct = round((payload.student_count / max(hostel.capacity, 1)) * 100, 2)
    hostel.current_occupancy = payload.student_count

    existing = db.query(Occupancy).filter(
        Occupancy.hostel_id == payload.hostel_id,
        Occupancy.date == payload.date
    ).first()

    if existing:
        existing.student_count = payload.student_count
        existing.occupancy_percentage = occ_pct
        db.commit()
        db.refresh(existing)
        target = existing
    else:
        new_occ = Occupancy(
            hostel_id=payload.hostel_id,
            date=payload.date,
            student_count=payload.student_count,
            occupancy_percentage=occ_pct
        )
        db.add(new_occ)
        db.commit()
        db.refresh(new_occ)
        target = new_occ

    return OccupancyResponse(
        id=target.id,
        hostel_id=target.hostel_id,
        hostel_name=hostel.name,
        hostel_block=hostel.block,
        date=target.date,
        student_count=target.student_count,
        occupancy_percentage=target.occupancy_percentage
    )
