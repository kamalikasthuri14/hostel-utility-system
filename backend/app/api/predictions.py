from fastapi import APIRouter, Depends, Query, HTTPException
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
