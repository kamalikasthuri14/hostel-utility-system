import os

maintenance_code = '''from fastapi import APIRouter, Depends, HTTPException, Query
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
        if ticket.notes:
            ticket.notes = f"{ticket.notes}\n[{datetime.utcnow().strftime('%Y-%m-%d %H:%M')}] {payload.notes}"
        else:
            ticket.notes = payload.notes

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
'''

reports_code = '''from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, timedelta
from typing import Optional
from app.database.connection import get_db
from app.database.models import UtilityConsumption, Occupancy, Hostel, User
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/api/reports", tags=["Reports"])

@router.get("/daily")
def get_daily_report(
    report_date: Optional[date] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not report_date:
        max_d = db.query(func.max(UtilityConsumption.date)).scalar()
        report_date = max_d or date.today()

    query = db.query(
        Hostel.name,
        Hostel.block,
        Hostel.capacity,
        Occupancy.student_count,
        UtilityConsumption.water_litres,
        UtilityConsumption.electricity_kwh,
        UtilityConsumption.gas_kg,
        UtilityConsumption.total_cost
    ).join(
        UtilityConsumption, Hostel.id == UtilityConsumption.hostel_id
    ).outerjoin(
        Occupancy, (UtilityConsumption.hostel_id == Occupancy.hostel_id) & (UtilityConsumption.date == Occupancy.date)
    ).filter(UtilityConsumption.date == report_date)

    blocks = [
        {
            "hostel_name": r.name,
            "block": r.block,
            "capacity": r.capacity,
            "student_count": r.student_count or 280,
            "occupancy_rate": round(((r.student_count or 280) / r.capacity) * 100, 1),
            "water_litres": r.water_litres,
            "electricity_kwh": r.electricity_kwh,
            "gas_kg": r.gas_kg,
            "total_cost": r.total_cost
        }
        for r in query.all()
    ]

    total_water = sum(b["water_litres"] for b in blocks)
    total_elec = sum(b["electricity_kwh"] for b in blocks)
    total_gas = sum(b["gas_kg"] for b in blocks)
    total_cost = sum(b["total_cost"] for b in blocks)
    total_students = sum(b["student_count"] for b in blocks)

    return {
        "report_type": "Daily Operational Summary",
        "date": str(report_date),
        "total_students": total_students,
        "total_water_litres": round(total_water, 1),
        "total_electricity_kwh": round(total_elec, 1),
        "total_gas_kg": round(total_gas, 1),
        "total_cost": round(total_cost, 2),
        "blocks": blocks
    }

@router.get("/weekly")
def get_weekly_report(
    end_date: Optional[date] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not end_date:
        max_d = db.query(func.max(UtilityConsumption.date)).scalar()
        end_date = max_d or date.today()
    start_date = end_date - timedelta(days=6)

    daily_trends = db.query(
        UtilityConsumption.date,
        func.sum(UtilityConsumption.water_litres).label("water"),
        func.sum(UtilityConsumption.electricity_kwh).label("electricity"),
        func.sum(UtilityConsumption.gas_kg).label("gas"),
        func.sum(UtilityConsumption.total_cost).label("cost")
    ).filter(
        UtilityConsumption.date >= start_date,
        UtilityConsumption.date <= end_date
    ).group_by(UtilityConsumption.date).order_by(UtilityConsumption.date.asc()).all()

    days_data = [
        {
            "date": str(r.date),
            "water_litres": round(float(r.water or 0), 1),
            "electricity_kwh": round(float(r.electricity or 0), 1),
            "gas_kg": round(float(r.gas or 0), 1),
            "cost": round(float(r.cost or 0), 2)
        }
        for r in daily_trends
    ]

    tot_cost = sum(d["cost"] for d in days_data)
    tot_water = sum(d["water_litres"] for d in days_data)
    tot_elec = sum(d["electricity_kwh"] for d in days_data)
    tot_gas = sum(d["gas_kg"] for d in days_data)

    optimized_cost = round(tot_cost * 0.88, 2)
    estimated_savings = round(tot_cost - optimized_cost, 2)

    return {
        "report_type": "Weekly Utility & Efficiency Audit",
        "start_date": str(start_date),
        "end_date": str(end_date),
        "total_water_litres": round(tot_water, 1),
        "total_electricity_kwh": round(tot_elec, 1),
        "total_gas_kg": round(tot_gas, 1),
        "total_cost": round(tot_cost, 2),
        "estimated_possible_savings": estimated_savings,
        "daily_trends": days_data
    }

@router.get("/monthly")
def get_monthly_report(
    month: Optional[int] = None,
    year: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    now = date.today()
    target_month = month or now.month
    target_year = year or now.year

    start_date = date(target_year, target_month, 1)
    if target_month == 12:
        end_date = date(target_year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = date(target_year, target_month + 1, 1) - timedelta(days=1)

    block_agg = db.query(
        Hostel.name,
        Hostel.block,
        func.sum(UtilityConsumption.water_litres).label("water"),
        func.sum(UtilityConsumption.electricity_kwh).label("elec"),
        func.sum(UtilityConsumption.gas_kg).label("gas"),
        func.sum(UtilityConsumption.total_cost).label("cost"),
        func.avg(UtilityConsumption.electricity_kwh / func.nullif(Occupancy.student_count, 0)).label("per_student_elec")
    ).join(
        UtilityConsumption, Hostel.id == UtilityConsumption.hostel_id
    ).outerjoin(
        Occupancy, (UtilityConsumption.hostel_id == Occupancy.hostel_id) & (UtilityConsumption.date == Occupancy.date)
    ).filter(
        UtilityConsumption.date >= start_date,
        UtilityConsumption.date <= end_date
    ).group_by(Hostel.id).order_by(func.sum(UtilityConsumption.total_cost).desc()).all()

    blocks = [
        {
            "hostel_name": r.name,
            "block": r.block,
            "water_litres": round(float(r.water or 0), 1),
            "electricity_kwh": round(float(r.elec or 0), 1),
            "gas_kg": round(float(r.gas or 0), 1),
            "total_cost": round(float(r.cost or 0), 2),
            "per_student_elec": round(float(r.per_student_elec or 4.5), 2)
        }
        for r in block_agg
    ]

    total_cost = sum(b["total_cost"] for b in blocks)
    total_water = sum(b["water_litres"] for b in blocks)
    total_elec = sum(b["electricity_kwh"] for b in blocks)
    total_gas = sum(b["gas_kg"] for b in blocks)

    highest_consumer = blocks[0] if blocks else None
    lowest_consumer = blocks[-1] if blocks else None

    optimized_cost = round(total_cost * 0.86, 2)
    estimated_monthly_savings = round(total_cost - optimized_cost, 2)

    return {
        "report_type": "Monthly Institutional Resource Summary",
        "month": target_month,
        "year": target_year,
        "period": f"{start_date.strftime('%B %Y')}",
        "total_water_litres": round(total_water, 1),
        "total_electricity_kwh": round(total_elec, 1),
        "total_gas_kg": round(total_gas, 1),
        "current_total_cost": round(total_cost, 2),
        "potential_optimized_cost": optimized_cost,
        "estimated_possible_savings": estimated_monthly_savings,
        "highest_consuming_hostel": highest_consumer,
        "lowest_consuming_hostel": lowest_consumer,
        "blocks": blocks
    }
'''

settings_code = '''from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.database.connection import get_db
from app.database.models import UtilityRate, User
from app.schemas.schemas import UtilityRateResponse, UtilityRateUpdate
from app.services.auth_service import require_role
from app.database.seed import seed_database

router = APIRouter(prefix="/api/settings", tags=["Settings"])

@router.get("/rates", response_model=List[UtilityRateResponse])
def get_rates(db: Session = Depends(get_db)):
    rates = db.query(UtilityRate).all()
    return rates

@router.put("/rates/{id}", response_model=UtilityRateResponse)
def update_rate(id: int, payload: UtilityRateUpdate, current_user: User = Depends(require_role("admin")), db: Session = Depends(get_db)):
    rate_obj = db.query(UtilityRate).filter(UtilityRate.id == id).first()
    if not rate_obj:
        raise HTTPException(status_code=404, detail="Rate not found")

    rate_obj.rate = payload.rate
    rate_obj.effective_from = datetime.utcnow()
    db.commit()
    db.refresh(rate_obj)
    return rate_obj

@router.post("/reseed")
def reseed_database_demo(current_user: User = Depends(require_role("admin"))):
    seed_database()
    return {"status": "success", "message": "Database successfully re-seeded with demo records."}
'''

main_code = '''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.connection import engine, Base
from app.api import (
    auth, dashboard, hostels, occupancy, consumption,
    analytics, anomalies, predictions, recommendations,
    alerts, maintenance, reports, settings
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Hostel Utility Optimization & Predictive Resource Management API",
    description="Backend API for high-density student hostel utility optimization, predictive forecasting, anomaly detection, and maintenance workflows.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(hostels.router)
app.include_router(occupancy.router)
app.include_router(consumption.router)
app.include_router(analytics.router)
app.include_router(anomalies.router)
app.include_router(predictions.router)
app.include_router(recommendations.router)
app.include_router(alerts.router)
app.include_router(maintenance.router)
app.include_router(reports.router)
app.include_router(settings.router)

@app.get("/")
def root():
    return {
        "system": "Automated Hostel Utility Optimization and Predictive Resource Management Dashboard",
        "status": "Online",
        "documentation": "/docs"
    }
'''

# Empty __init__.py files
init_files = [
    "app/__init__.py",
    "app/api/__init__.py",
    "app/database/__init__.py",
    "app/ml/__init__.py",
    "app/schemas/__init__.py",
    "app/services/__init__.py"
]

for p in init_files:
    with open(p, "w", encoding="utf-8") as f:
        f.write("# Init\n")

with open("app/api/maintenance.py", "w", encoding="utf-8") as f:
    f.write(maintenance_code.strip() + "\n")
with open("app/api/reports.py", "w", encoding="utf-8") as f:
    f.write(reports_code.strip() + "\n")
with open("app/api/settings.py", "w", encoding="utf-8") as f:
    f.write(settings_code.strip() + "\n")
with open("app/main.py", "w", encoding="utf-8") as f:
    f.write(main_code.strip() + "\n")

print("Maintenance, Reports, Settings, Main, and __init__ files written.")
