from fastapi import APIRouter, Depends, Query
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
        "period": start_date.strftime("%B %Y"),
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
