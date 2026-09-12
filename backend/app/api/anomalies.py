from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.database.models import User
from app.services.auth_service import get_current_user, require_role
from app.ml.anomaly_detection import run_anomaly_detection

router = APIRouter(prefix="/api/anomalies", tags=["Anomalies"])

@router.post("/detect")
def trigger_anomaly_detection(current_user: User = Depends(require_role("admin", "warden")), db: Session = Depends(get_db)):
    detected = run_anomaly_detection(db)
    return {
        "status": "success",
        "message": f"Anomaly detection completed. {len(detected)} anomaly events identified.",
        "anomalies": detected
    }
