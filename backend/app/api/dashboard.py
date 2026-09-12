from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, timedelta
from app.database.connection import get_db
from app.database.models import User, Hostel, Occupancy, UtilityConsumption, Alert
from app.services.auth_service import get_current_user
from app.ml.efficiency import calculate_hostel_efficiency

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/summary")
def get_dashboard_summary(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    hostel_id = current_user.assigned_hostel_id if current_user.role == "warden" else None

    hostel_query = db.query(Hostel)
    if hostel_id:
        hostel_query = hostel_query.filter(Hostel.id == hostel_id)
    hostels = hostel_query.all()
    total_blocks = len(hostels)
    total_capacity = sum(h.capacity for h in hostels)

    latest_date_row = db.query(func.max(UtilityConsumption.date)).first()
    latest_date = latest_date_row[0] if latest_date_row and latest_date_row[0] else date.today()

    cons_query = db.query(
        func.sum(UtilityConsumption.water_litres).label("water"),
        func.sum(UtilityConsumption.electricity_kwh).label("electricity"),
        func.sum(UtilityConsumption.gas_kg).label("gas"),
        func.sum(UtilityConsumption.total_cost).label("cost")
    ).filter(UtilityConsumption.date == latest_date)

    if hostel_id:
        cons_query = cons_query.filter(UtilityConsumption.hostel_id == hostel_id)

    today_cons = cons_query.first()

    occ_query = db.query(func.sum(Occupancy.student_count)).filter(Occupancy.date == latest_date)
    if hostel_id:
        occ_query = occ_query.filter(Occupancy.hostel_id == hostel_id)
    total_students = occ_query.scalar() or sum(h.current_occupancy for h in hostels)

    alert_query = db.query(func.count(Alert.id)).filter(Alert.status == "Active")
    if hostel_id:
        alert_query = alert_query.filter(Alert.hostel_id == hostel_id)
    active_alerts_count = alert_query.scalar() or 0

    eff = calculate_hostel_efficiency(db, hostel_id=hostel_id)

    trend_start = latest_date - timedelta(days=6)
    trends_query = db.query(
        UtilityConsumption.date,
        func.sum(UtilityConsumption.water_litres).label("water"),
        func.sum(UtilityConsumption.electricity_kwh).label("electricity"),
        func.sum(UtilityConsumption.gas_kg).label("gas"),
        func.sum(UtilityConsumption.total_cost).label("cost")
    ).filter(UtilityConsumption.date >= trend_start, UtilityConsumption.date <= latest_date)

    if hostel_id:
        trends_query = trends_query.filter(UtilityConsumption.hostel_id == hostel_id)

    trends_raw = trends_query.group_by(UtilityConsumption.date).order_by(UtilityConsumption.date.asc()).all()
    
    seven_day_trends = [
        {
            "date": str(r.date),
            "water_litres": round(float(r.water or 0), 1),
            "electricity_kwh": round(float(r.electricity or 0), 1),
            "gas_kg": round(float(r.gas or 0), 1),
            "total_cost": round(float(r.cost or 0), 2)
        }
        for r in trends_raw
    ]

    recent_alerts_query = db.query(Alert, Hostel.name, Hostel.block).join(
        Hostel, Alert.hostel_id == Hostel.id
    ).filter(Alert.status == "Active")
    if hostel_id:
        recent_alerts_query = recent_alerts_query.filter(Alert.hostel_id == hostel_id)
    recent_alerts_query = recent_alerts_query.order_by(Alert.created_at.desc()).limit(5)

    recent_alerts = [
        {
            "id": a.Alert.id,
            "hostel_name": a.name,
            "hostel_block": a.block,
            "resource_type": a.Alert.resource_type,
            "severity": a.Alert.severity,
            "difference_percentage": a.Alert.difference_percentage,
            "description": a.Alert.description,
            "created_at": a.Alert.created_at.isoformat()
        }
        for a in recent_alerts_query.all()
    ]

    return {
        "summary": {
            "total_students": int(total_students),
            "total_hostel_blocks": total_blocks,
            "total_capacity": total_capacity,
            "overall_occupancy_rate": round((total_students / max(total_capacity, 1)) * 100, 1),
            "water_today_litres": round(float(today_cons.water or 0), 1),
            "electricity_today_kwh": round(float(today_cons.electricity or 0), 1),
            "gas_today_kg": round(float(today_cons.gas or 0), 1),
            "estimated_cost_today": round(float(today_cons.cost or 0), 2),
            "active_alerts": active_alerts_count,
            "efficiency_score": eff["overall_score"],
            "efficiency_grade": eff["grade"],
            "efficiency_rating": eff["rating"],
            "latest_date": str(latest_date)
        },
        "efficiency_details": eff,
        "seven_day_trends": seven_day_trends,
        "recent_alerts": recent_alerts
    }

@router.get("/efficiency")
def get_efficiency(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    hostel_id = current_user.assigned_hostel_id if current_user.role == "warden" else None
    return calculate_hostel_efficiency(db, hostel_id=hostel_id)
