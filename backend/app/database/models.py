import datetime
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
