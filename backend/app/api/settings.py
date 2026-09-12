from fastapi import APIRouter, Depends, HTTPException
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
