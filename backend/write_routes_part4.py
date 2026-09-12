import os

alerts_code = '''from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.database.connection import get_db
from app.database.models import Alert, Hostel, Maintenance, User
from app.schemas.schemas import AlertResponse, AlertUpdate, ConvertAlertToMaintenanceRequest
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/api/alerts", tags=["Alerts"])

@router.get("", response_model=List[AlertResponse])
def get_alerts(
    hostel_id: Optional[int] = None,
    severity: Optional[str] = None,
    resource_type: Optional[str] = None,
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Alert, Hostel.name, Hostel.block).join(Hostel, Alert.hostel_id == Hostel.id)

    if current_user.role == "warden" and current_user.assigned_hostel_id:
        query = query.filter(Alert.hostel_id == current_user.assigned_hostel_id)
    elif hostel_id:
        query = query.filter(Alert.hostel_id == hostel_id)

    if severity:
        query = query.filter(Alert.severity == severity)
    if resource_type:
        query = query.filter(Alert.resource_type == resource_type)
    if status:
        query = query.filter(Alert.status == status)

    records = query.order_by(Alert.created_at.desc()).all()

    results = []
    for r in records:
        a = r.Alert
        results.append(AlertResponse(
            id=a.id,
            hostel_id=a.hostel_id,
            hostel_name=r.name,
            hostel_block=r.block,
            resource_type=a.resource_type,
            severity=a.severity,
            actual_value=a.actual_value,
            expected_value=a.expected_value,
            difference_percentage=a.difference_percentage,
            description=a.description,
            status=a.status,
            created_at=a.created_at
        ))
    return results

@router.put("/{id}", response_model=AlertResponse)
def update_alert_status(id: int, payload: AlertUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    a = db.query(Alert).filter(Alert.id == id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Alert not found")

    a.status = payload.status
    db.commit()
    db.refresh(a)

    h = db.query(Hostel).filter(Hostel.id == a.hostel_id).first()
    return AlertResponse(
        id=a.id,
        hostel_id=a.hostel_id,
        hostel_name=h.name if h else "",
        hostel_block=h.block if h else "",
        resource_type=a.resource_type,
        severity=a.severity,
        actual_value=a.actual_value,
        expected_value=a.expected_value,
        difference_percentage=a.difference_percentage,
        description=a.description,
        status=a.status,
        created_at=a.created_at
    )

@router.post("/{id}/convert-to-ticket")
def convert_alert_to_ticket(id: int, payload: ConvertAlertToMaintenanceRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    a = db.query(Alert).filter(Alert.id == id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Alert not found")

    issue_type_map = {
        "Water": "Pipeline Leak / Overflow Anomaly",
        "Electricity": "Power Surge / Appliance Overdraw",
        "Gas": "LPG Burner / Pressure Leakage"
    }

    ticket = Maintenance(
        hostel_id=a.hostel_id,
        resource_type=a.resource_type,
        issue_type=issue_type_map.get(a.resource_type, "Utility Anomaly"),
        description=f"Generated from Alert #{a.id}: {a.description}",
        priority=payload.priority or a.severity,
        assigned_to=payload.assigned_to or "Vikram Singh",
        status="Assigned",
        created_at=datetime.utcnow(),
        notes=payload.notes or f"Auto-escalated by {current_user.name}."
    )
    db.add(ticket)
    a.status = "Reviewed"
    db.commit()
    db.refresh(ticket)

    return {
        "status": "success",
        "message": f"Alert converted into Maintenance Ticket #{ticket.id}",
        "ticket_id": ticket.id
    }
'''

predictions_code = '''from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.database.connection import get_db
from app.database.models import User
from app.schemas.schemas import PredictionResponse
from app.services.auth_service import get_current_user
from app.ml.prediction import generate_7day_prediction, train_and_save_all_models

router = APIRouter(prefix="/api/predictions", tags=["Predictions"])

@router.get("", response_model=PredictionResponse)
def get_predictions(
    hostel_id: Optional[int] = None,
    resource_type: str = Query("Electricity", enum=["Electricity", "Water", "Gas", "Cost"]),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role == "warden" and current_user.assigned_hostel_id:
        hostel_id = current_user.assigned_hostel_id

    try:
        pred_data = generate_7day_prediction(db, hostel_id=hostel_id, resource_type=resource_type)
        return pred_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/retrain")
def retrain_ml_models(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    res = train_and_save_all_models(db)
    return res
'''

recommendations_code = '''from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.connection import get_db
from app.database.models import User
from app.schemas.schemas import RecommendationItem
from app.services.auth_service import get_current_user
from app.ml.explainability import generate_actionable_recommendations

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])

@router.get("", response_model=List[RecommendationItem])
def get_recommendations(
    hostel_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role == "warden" and current_user.assigned_hostel_id:
        hostel_id = current_user.assigned_hostel_id

    recs = generate_actionable_recommendations(db, hostel_id=hostel_id)
    return recs
'''

with open("app/api/alerts.py", "w", encoding="utf-8") as f:
    f.write(alerts_code.strip() + "\n")
with open("app/api/predictions.py", "w", encoding="utf-8") as f:
    f.write(predictions_code.strip() + "\n")
with open("app/api/recommendations.py", "w", encoding="utf-8") as f:
    f.write(recommendations_code.strip() + "\n")
print("Alerts, Predictions, and Recommendations routes written.")
