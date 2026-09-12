import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

files = {}

# 1. Connection & Config
files["app/database/connection.py"] = '''import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "hostel_utility.db")
    DATABASE_URL = f"sqlite:///{db_path}"

# SQLite specific config
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''

# 2. Database Models
files["app/database/models.py"] = '''import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, Date, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from app.database.connection import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="warden") # admin, warden, maintenance
    assigned_hostel_id = Column(Integer, ForeignKey("hostels.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    assigned_hostel = relationship("Hostel", back_populates="wardens", foreign_keys=[assigned_hostel_id])

class Hostel(Base):
    __tablename__ = "hostels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    block = Column(String(50), nullable=False, unique=True) # e.g. Block A, Block B
    capacity = Column(Integer, nullable=False)
    current_occupancy = Column(Integer, default=0)
    location = Column(String(200), default="North Campus")
    status = Column(String(50), default="Active") # Active, Maintenance, Inactive
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    wardens = relationship("User", back_populates="assigned_hostel")
    occupancy_records = relationship("Occupancy", back_populates="hostel", cascade="all, delete-orphan")
    consumption_records = relationship("UtilityConsumption", back_populates="hostel", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="hostel", cascade="all, delete-orphan")
    predictions = relationship("Prediction", back_populates="hostel", cascade="all, delete-orphan")
    maintenance_issues = relationship("Maintenance", back_populates="hostel", cascade="all, delete-orphan")

class Occupancy(Base):
    __tablename__ = "occupancy"

    id = Column(Integer, primary_key=True, index=True)
    hostel_id = Column(Integer, ForeignKey("hostels.id"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    student_count = Column(Integer, nullable=False)
    occupancy_percentage = Column(Float, nullable=False)

    hostel = relationship("Hostel", back_populates="occupancy_records")

class UtilityConsumption(Base):
    __tablename__ = "utility_consumption"

    id = Column(Integer, primary_key=True, index=True)
    hostel_id = Column(Integer, ForeignKey("hostels.id"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    water_litres = Column(Float, nullable=False)
    electricity_kwh = Column(Float, nullable=False)
    gas_kg = Column(Float, nullable=False)
    water_cost = Column(Float, nullable=False)
    electricity_cost = Column(Float, nullable=False)
    gas_cost = Column(Float, nullable=False)
    total_cost = Column(Float, nullable=False)

    hostel = relationship("Hostel", back_populates="consumption_records")

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    hostel_id = Column(Integer, ForeignKey("hostels.id"), nullable=False, index=True)
    resource_type = Column(String(50), nullable=False) # Water, Electricity, Gas
    severity = Column(String(50), nullable=False) # Low, Medium, High, Critical
    actual_value = Column(Float, nullable=False)
    expected_value = Column(Float, nullable=False)
    difference_percentage = Column(Float, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(50), default="Active") # Active, Reviewed, Resolved
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    hostel = relationship("Hostel", back_populates="alerts")

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    hostel_id = Column(Integer, ForeignKey("hostels.id"), nullable=False, index=True)
    resource_type = Column(String(50), nullable=False) # Water, Electricity, Gas, Total Cost
    prediction_date = Column(Date, nullable=False, index=True)
    predicted_value = Column(Float, nullable=False)
    actual_value = Column(Float, nullable=True)
    model_name = Column(String(100), default="RandomForestRegressor")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    hostel = relationship("Hostel", back_populates="predictions")

class Maintenance(Base):
    __tablename__ = "maintenance"

    id = Column(Integer, primary_key=True, index=True)
    hostel_id = Column(Integer, ForeignKey("hostels.id"), nullable=False, index=True)
    resource_type = Column(String(50), nullable=False) # Water, Electricity, Gas, General
    issue_type = Column(String(100), nullable=False) # Pipeline Leak, Meter Anomaly, HVAC Overuse, Valve Malfunction, etc.
    description = Column(Text, nullable=False)
    priority = Column(String(50), default="Medium") # Low, Medium, High, Critical
    assigned_to = Column(String(100), nullable=True) # Staff Name / ID
    status = Column(String(50), default="Open") # Open, Assigned, In Progress, Resolved, Closed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)

    hostel = relationship("Hostel", back_populates="maintenance_issues")

class UtilityRate(Base):
    __tablename__ = "utility_rates"

    id = Column(Integer, primary_key=True, index=True)
    resource_type = Column(String(50), unique=True, nullable=False) # Electricity, Water, Gas
    rate = Column(Float, nullable=False) # Rate per unit
    unit = Column(String(50), nullable=False) # kWh, Litres, kg
    effective_from = Column(DateTime, default=datetime.datetime.utcnow)
'''

# 3. Auth & Security Service
files["app/services/auth_service.py"] = '''import os
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.database.models import User

SECRET_KEY = os.getenv("JWT_SECRET", "super-secret-hostel-utility-key-2026-secure")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 # 24 hours

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

def require_role(*roles):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in roles and "admin" not in roles:
            # If admin is allowed or user role matches
            if current_user.role != "admin" and current_user.role not in roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Operation not permitted for role: {current_user.role}"
                )
        return current_user
    return role_checker
'''

for rel_path, content in files.items():
    full_path = os.path.join(BASE_DIR, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {rel_path}")

print("Backend base files created successfully.")
