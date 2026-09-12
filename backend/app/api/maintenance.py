from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.database.connection import get_db
from app.database.models import Maintenance, Hostel, User
from app.schemas.schemas import MaintenanceCreate, MaintenanceUpdate, MaintenanceResponse
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/api/maintenance", tags=["Maintenance"])

@router.get("", response_model=List[MaintenanceResponse])
def get_maintenance_tickets(
    hostel_id: Optional[int] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Maintenance, Hostel.name, Hostel.block).join(Hostel, Maintenance.hostel_id == Hostel.id)

    if current_user.role == "warden" and current_user.assigned_hostel_id:
        query = query.filter(Maintenance.hostel_id == current_user.assigned_hostel_id)
    elif hostel_id:
        query = query.filter(Maintenance.hostel_id == hostel_id)

    if status:
        query = query.filter(Maintenance.status == status)
    if priority:
        query = query.filter(Maintenance.priority == priority)

    records = query.order_by(Maintenance.created_at.desc()).all()

    results = []
    for r in records:
        m = r.Maintenance
        results.append(MaintenanceResponse(
            id=m.id,
            hostel_id=m.hostel_id,
            hostel_name=r.name,
            hostel_block=r.block,
            resource_type=m.resource_type,
            issue_type=m.issue_type,
            description=m.description,
            priority=m.priority,
            assigned_to=m.assigned_to,
            status=m.status,
            created_at=m.created_at,
            resolved_at=m.resolved_at,
            notes=m.notes
        ))
    return results

@router.post("", response_model=MaintenanceResponse)
def create_maintenance_ticket(payload: MaintenanceCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    hostel = db.query(Hostel).filter(Hostel.id == payload.hostel_id).first()
    if not hostel:
        raise HTTPException(status_code=404, detail="Hostel not found")

    ticket = Maintenance(
        hostel_id=payload.hostel_id,
        resource_type=payload.resource_type,
        issue_type=payload.issue_type,
        description=payload.description,
        priority=payload.priority or "Medium",
        assigned_to=payload.assigned_to,
        status="Open" if not payload.assigned_to else "Assigned",
        created_at=datetime.utcnow(),
        notes=payload.notes
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return MaintenanceResponse(
        id=ticket.id,
        hostel_id=ticket.hostel_id,
        hostel_name=hostel.name,
        hostel_block=hostel.block,
        resource_type=ticket.resource_type,
        issue_type=ticket.issue_type,
        description=ticket.description,
        priority=ticket.priority,
        assigned_to=ticket.assigned_to,
        status=ticket.status,
        created_at=ticket.created_at,
        resolved_at=ticket.resolved_at,
        notes=ticket.notes
    )

@router.put("/{id}", response_model=MaintenanceResponse)
def update_maintenance_ticket(id: int, payload: MaintenanceUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    ticket = db.query(Maintenance).filter(Maintenance.id == id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    if payload.priority:
        ticket.priority = payload.priority
    if payload.assigned_to:
        ticket.assigned_to = payload.assigned_to
        if ticket.status == "Open":
            ticket.status = "Assigned"
    if payload.status:
        ticket.status = payload.status
        if payload.status in ["Resolved", "Closed"] and not ticket.resolved_at:
            ticket.resolved_at = datetime.utcnow()
    if payload.notes:
        now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M")
        if ticket.notes:
            ticket.notes = ticket.notes + f"\n[{now_str}] " + payload.notes
        else:
            ticket.notes = f"[{now_str}] " + payload.notes

    db.commit()
    db.refresh(ticket)

    hostel = db.query(Hostel).filter(Hostel.id == ticket.hostel_id).first()
    return MaintenanceResponse(
        id=ticket.id,
        hostel_id=ticket.hostel_id,
        hostel_name=hostel.name if hostel else "",
        hostel_block=hostel.block if hostel else "",
        resource_type=ticket.resource_type,
        issue_type=ticket.issue_type,
        description=ticket.description,
        priority=ticket.priority,
        assigned_to=ticket.assigned_to,
        status=ticket.status,
        created_at=ticket.created_at,
        resolved_at=ticket.resolved_at,
        notes=ticket.notes
    )
