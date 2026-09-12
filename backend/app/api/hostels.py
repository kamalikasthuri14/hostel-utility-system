from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.database.models import Hostel, User
from app.schemas.schemas import HostelCreate, HostelUpdate, HostelResponse
from app.services.auth_service import get_current_user, require_role

router = APIRouter(prefix="/api/hostels", tags=["Hostels"])

@router.get("", response_model=List[HostelResponse])
def list_hostels(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    query = db.query(Hostel)
    if current_user.role == "warden" and current_user.assigned_hostel_id:
        query = query.filter(Hostel.id == current_user.assigned_hostel_id)

    hostels = query.order_by(Hostel.block.asc()).all()
    results = []
    for h in hostels:
        occ_rate = round((h.current_occupancy / max(h.capacity, 1)) * 100, 1)
        res = HostelResponse(
            id=h.id,
            name=h.name,
            block=h.block,
            capacity=h.capacity,
            current_occupancy=h.current_occupancy,
            location=h.location,
            status=h.status,
            created_at=h.created_at,
            occupancy_rate=occ_rate
        )
        results.append(res)
    return results

@router.get("/{id}", response_model=HostelResponse)
def get_hostel(id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    h = db.query(Hostel).filter(Hostel.id == id).first()
    if not h:
        raise HTTPException(status_code=404, detail="Hostel not found")
    occ_rate = round((h.current_occupancy / max(h.capacity, 1)) * 100, 1)
    return HostelResponse(
        id=h.id,
        name=h.name,
        block=h.block,
        capacity=h.capacity,
        current_occupancy=h.current_occupancy,
        location=h.location,
        status=h.status,
        created_at=h.created_at,
        occupancy_rate=occ_rate
    )

@router.post("", response_model=HostelResponse)
def create_hostel(payload: HostelCreate, current_user: User = Depends(require_role("admin")), db: Session = Depends(get_db)):
    existing = db.query(Hostel).filter(Hostel.block == payload.block.strip()).first()
    if existing:
        raise HTTPException(status_code=400, detail="Hostel block already exists")

    h = Hostel(
        name=payload.name,
        block=payload.block,
        capacity=payload.capacity,
        current_occupancy=payload.current_occupancy or 0,
        location=payload.location or "Campus",
        status=payload.status or "Active"
    )
    db.add(h)
    db.commit()
    db.refresh(h)
    return HostelResponse(
        id=h.id,
        name=h.name,
        block=h.block,
        capacity=h.capacity,
        current_occupancy=h.current_occupancy,
        location=h.location,
        status=h.status,
        created_at=h.created_at,
        occupancy_rate=round((h.current_occupancy / max(h.capacity, 1)) * 100, 1)
    )

@router.put("/{id}", response_model=HostelResponse)
def update_hostel(id: int, payload: HostelUpdate, current_user: User = Depends(require_role("admin")), db: Session = Depends(get_db)):
    h = db.query(Hostel).filter(Hostel.id == id).first()
    if not h:
        raise HTTPException(status_code=404, detail="Hostel not found")

    for field, val in payload.dict(exclude_unset=True).items():
        setattr(h, field, val)

    db.commit()
    db.refresh(h)
    return HostelResponse(
        id=h.id,
        name=h.name,
        block=h.block,
        capacity=h.capacity,
        current_occupancy=h.current_occupancy,
        location=h.location,
        status=h.status,
        created_at=h.created_at,
        occupancy_rate=round((h.current_occupancy / max(h.capacity, 1)) * 100, 1)
    )

@router.delete("/{id}")
def delete_hostel(id: int, current_user: User = Depends(require_role("admin")), db: Session = Depends(get_db)):
    h = db.query(Hostel).filter(Hostel.id == id).first()
    if not h:
        raise HTTPException(status_code=404, detail="Hostel not found")
    db.delete(h)
    db.commit()
    return {"status": "success", "message": f"Hostel {h.name} deleted successfully"}
