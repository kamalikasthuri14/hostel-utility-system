from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from datetime import date, timedelta
from app.database.connection import get_db
from app.database.models import UtilityConsumption, Occupancy, Hostel, User
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

@router.get("/water")
def get_water_analytics(
    hostel_id: Optional[int] = None,
    days: int = Query(30, ge=7, le=180),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role == "warden" and current_user.assigned_hostel_id:
        hostel_id = current_user.assigned_hostel_id

    start_date = date.today() - timedelta(days=days)

    daily_query = db.query(
        UtilityConsumption.date,
        func.sum(UtilityConsumption.water_litres).label("water"),
        func.sum(UtilityConsumption.water_cost).label("cost")
    ).filter(UtilityConsumption.date >= start_date)

    if hostel_id:
        daily_query = daily_query.filter(UtilityConsumption.hostel_id == hostel_id)

    daily_data = [
        {"date": str(r.date), "water_litres": round(float(r.water or 0), 1), "cost": round(float(r.cost or 0), 2)}
        for r in daily_query.group_by(UtilityConsumption.date).order_by(UtilityConsumption.date.asc()).all()
    ]

    hostel_comp_query = db.query(
        Hostel.name,
        Hostel.block,
        func.sum(UtilityConsumption.water_litres).label("total_water"),
        func.avg(UtilityConsumption.water_litres).label("avg_daily_water"),
        func.avg(UtilityConsumption.water_litres / func.nullif(Occupancy.student_count, 0)).label("per_student_water")
    ).join(
        UtilityConsumption, Hostel.id == UtilityConsumption.hostel_id
    ).outerjoin(
        Occupancy, (UtilityConsumption.hostel_id == Occupancy.hostel_id) & (UtilityConsumption.date == Occupancy.date)
    ).filter(UtilityConsumption.date >= start_date).group_by(Hostel.id)

    hostel_comparison = [
        {
            "hostel_name": r.name,
            "block": r.block,
            "total_water_litres": round(float(r.total_water or 0), 1),
            "avg_daily_water": round(float(r.avg_daily_water or 0), 1),
            "per_student_water": round(float(r.per_student_water or 95.0), 1)
        }
        for r in hostel_comp_query.all()
    ]

    return {
        "resource": "Water",
        "unit": "Litres",
        "daily_trends": daily_data,
        "hostel_comparison": hostel_comparison,
        "summary": {
            "total_consumption": sum(d["water_litres"] for d in daily_data),
            "avg_daily": round(sum(d["water_litres"] for d in daily_data) / max(len(daily_data), 1), 1),
            "total_cost": round(sum(d["cost"] for d in daily_data), 2)
        }
    }

@router.get("/electricity")
def get_electricity_analytics(
    hostel_id: Optional[int] = None,
    days: int = Query(30, ge=7, le=180),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role == "warden" and current_user.assigned_hostel_id:
        hostel_id = current_user.assigned_hostel_id

    start_date = date.today() - timedelta(days=days)

    daily_query = db.query(
        UtilityConsumption.date,
        func.sum(UtilityConsumption.electricity_kwh).label("electricity"),
        func.sum(UtilityConsumption.electricity_cost).label("cost")
    ).filter(UtilityConsumption.date >= start_date)

    if hostel_id:
        daily_query = daily_query.filter(UtilityConsumption.hostel_id == hostel_id)

    daily_data = [
        {"date": str(r.date), "electricity_kwh": round(float(r.electricity or 0), 1), "cost": round(float(r.cost or 0), 2)}
        for r in daily_query.group_by(UtilityConsumption.date).order_by(UtilityConsumption.date.asc()).all()
    ]

    hostel_comp_query = db.query(
        Hostel.name,
        Hostel.block,
        func.sum(UtilityConsumption.electricity_kwh).label("total_elec"),
        func.avg(UtilityConsumption.electricity_kwh).label("avg_daily_elec"),
        func.avg(UtilityConsumption.electricity_kwh / func.nullif(Occupancy.student_count, 0)).label("per_student_elec")
    ).join(
        UtilityConsumption, Hostel.id == UtilityConsumption.hostel_id
    ).outerjoin(
        Occupancy, (UtilityConsumption.hostel_id == Occupancy.hostel_id) & (UtilityConsumption.date == Occupancy.date)
    ).filter(UtilityConsumption.date >= start_date).group_by(Hostel.id)

    hostel_comparison = [
        {
            "hostel_name": r.name,
            "block": r.block,
            "total_electricity_kwh": round(float(r.total_elec or 0), 1),
            "avg_daily_electricity": round(float(r.avg_daily_elec or 0), 1),
            "per_student_electricity": round(float(r.per_student_elec or 4.5), 2)
        }
        for r in hostel_comp_query.all()
    ]

    peak_breakdown = [
        {"time_slot": "Morning Rush (06:00 - 09:00)", "share_pct": 34, "category": "Geysers & Lighting"},
        {"time_slot": "Day / Class Hours (09:00 - 17:00)", "share_pct": 18, "category": "Base / Common Areas"},
        {"time_slot": "Evening Study (17:00 - 23:00)", "share_pct": 38, "category": "Laptops, Lighting & ACs"},
        {"time_slot": "Night Phantom (23:00 - 06:00)", "share_pct": 10, "category": "Fans & Standby Loads"}
    ]

    return {
        "resource": "Electricity",
        "unit": "kWh",
        "daily_trends": daily_data,
        "hostel_comparison": hostel_comparison,
        "peak_breakdown": peak_breakdown,
        "summary": {
            "total_consumption": sum(d["electricity_kwh"] for d in daily_data),
            "avg_daily": round(sum(d["electricity_kwh"] for d in daily_data) / max(len(daily_data), 1), 1),
            "total_cost": round(sum(d["cost"] for d in daily_data), 2)
        }
    }

@router.get("/gas")
def get_gas_analytics(
    hostel_id: Optional[int] = None,
    days: int = Query(30, ge=7, le=180),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role == "warden" and current_user.assigned_hostel_id:
        hostel_id = current_user.assigned_hostel_id

    start_date = date.today() - timedelta(days=days)

    daily_query = db.query(
        UtilityConsumption.date,
        func.sum(UtilityConsumption.gas_kg).label("gas"),
        func.sum(UtilityConsumption.gas_cost).label("cost")
    ).filter(UtilityConsumption.date >= start_date)

    if hostel_id:
        daily_query = daily_query.filter(UtilityConsumption.hostel_id == hostel_id)

    daily_data = [
        {"date": str(r.date), "gas_kg": round(float(r.gas or 0), 1), "cost": round(float(r.cost or 0), 2)}
        for r in daily_query.group_by(UtilityConsumption.date).order_by(UtilityConsumption.date.asc()).all()
    ]

    hostel_comp_query = db.query(
        Hostel.name,
        Hostel.block,
        func.sum(UtilityConsumption.gas_kg).label("total_gas"),
        func.avg(UtilityConsumption.gas_kg).label("avg_daily_gas"),
        func.avg(UtilityConsumption.gas_kg / func.nullif(Occupancy.student_count, 0)).label("per_student_gas")
    ).join(
        UtilityConsumption, Hostel.id == UtilityConsumption.hostel_id
    ).outerjoin(
        Occupancy, (UtilityConsumption.hostel_id == Occupancy.hostel_id) & (UtilityConsumption.date == Occupancy.date)
    ).filter(UtilityConsumption.date >= start_date).group_by(Hostel.id)

    hostel_comparison = [
        {
            "hostel_name": r.name,
            "block": r.block,
            "total_gas_kg": round(float(r.total_gas or 0), 1),
            "avg_daily_gas": round(float(r.avg_daily_gas or 0), 1),
            "per_student_gas": round(float(r.per_student_gas or 0.14), 3)
        }
        for r in hostel_comp_query.all()
    ]

    return {
        "resource": "Gas",
        "unit": "kg",
        "daily_trends": daily_data,
        "hostel_comparison": hostel_comparison,
        "summary": {
            "total_consumption": sum(d["gas_kg"] for d in daily_data),
            "avg_daily": round(sum(d["gas_kg"] for d in daily_data) / max(len(daily_data), 1), 1),
            "total_cost": round(sum(d["cost"] for d in daily_data), 2)
        }
    }

@router.get("/per-student")
def get_per_student_analytics(
    days: int = Query(30, ge=7, le=180),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    start_date = date.today() - timedelta(days=days)

    query = db.query(
        Hostel.id,
        Hostel.name,
        Hostel.block,
        func.avg(Occupancy.student_count).label("avg_students"),
        func.avg(UtilityConsumption.water_litres / func.nullif(Occupancy.student_count, 0)).label("water_per_student"),
        func.avg(UtilityConsumption.electricity_kwh / func.nullif(Occupancy.student_count, 0)).label("elec_per_student"),
        func.avg(UtilityConsumption.gas_kg / func.nullif(Occupancy.student_count, 0)).label("gas_per_student")
    ).join(
        UtilityConsumption, Hostel.id == UtilityConsumption.hostel_id
    ).outerjoin(
        Occupancy, (UtilityConsumption.hostel_id == Occupancy.hostel_id) & (UtilityConsumption.date == Occupancy.date)
    ).filter(UtilityConsumption.date >= start_date).group_by(Hostel.id).order_by(Hostel.block.asc())

    records = query.all()
    data = []

    for r in records:
        w = round(float(r.water_per_student or 95.0), 1)
        e = round(float(r.elec_per_student or 4.5), 2)
        g = round(float(r.gas_per_student or 0.14), 3)

        is_water_high = w > 115.0
        is_elec_high = e > 5.2
        is_gas_high = g > 0.18

        data.append({
            "hostel_id": r.id,
            "hostel_name": r.name,
            "block": r.block,
            "avg_students": int(r.avg_students or 280),
            "water_l_per_student": w,
            "water_alert": is_water_high,
            "electricity_kwh_per_student": e,
            "electricity_alert": is_elec_high,
            "gas_kg_per_student": g,
            "gas_alert": is_gas_high,
            "cost_per_student_daily": round((w * 0.04) + (e * 8.5) + (g * 85.0), 2)
        })

    return {
        "benchmarks": {
            "recommended_water_L": 95.0,
            "recommended_electricity_kWh": 4.2,
            "recommended_gas_kg": 0.13
        },
        "hostels": data
    }
