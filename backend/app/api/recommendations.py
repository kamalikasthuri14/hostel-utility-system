from fastapi import APIRouter, Depends
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
