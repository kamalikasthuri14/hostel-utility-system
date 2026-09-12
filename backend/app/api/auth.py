from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.database.models import User, Hostel
from app.schemas.schemas import LoginRequest, Token, UserResponse
from app.services.auth_service import verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.strip().lower()).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    hostel_info = None
    if user.assigned_hostel_id:
        h = db.query(Hostel).filter(Hostel.id == user.assigned_hostel_id).first()
        if h:
            hostel_info = {"id": h.id, "name": h.name, "block": h.block}

    token = create_access_token(data={"sub": user.email, "role": user.role, "id": user.id})

    user_data = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "assigned_hostel": hostel_info
    }

    return {"access_token": token, "token_type": "bearer", "user": user_data}

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    hostel_info = None
    if current_user.assigned_hostel_id:
        h = db.query(Hostel).filter(Hostel.id == current_user.assigned_hostel_id).first()
        if h:
            hostel_info = {"id": h.id, "name": h.name, "block": h.block}

    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role,
        "assigned_hostel": hostel_info,
        "created_at": current_user.created_at
    }
