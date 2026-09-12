from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import date, datetime

# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    user: Dict[str, Any]

class LoginRequest(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    assigned_hostel_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Hostel Schemas
class HostelBase(BaseModel):
    name: str
    block: str
    capacity: int
    current_occupancy: Optional[int] = 0
    location: Optional[str] = "North Campus"
    status: Optional[str] = "Active"

class HostelCreate(HostelBase):
    pass

class HostelUpdate(BaseModel):
    name: Optional[str] = None
    block: Optional[str] = None
    capacity: Optional[int] = None
    current_occupancy: Optional[int] = None
    location: Optional[str] = None
    status: Optional[str] = None

class HostelResponse(HostelBase):
    id: int
    created_at: datetime
    occupancy_rate: Optional[float] = 0.0

    class Config:
        from_attributes = True

# Occupancy Schemas
class OccupancyCreate(BaseModel):
    hostel_id: int
    date: date
    student_count: int

class OccupancyResponse(BaseModel):
    id: int
    hostel_id: int
    hostel_name: Optional[str] = None
    hostel_block: Optional[str] = None
    date: date
    student_count: int
    occupancy_percentage: float

    class Config:
        from_attributes = True

# Utility Consumption Schemas
class ConsumptionCreate(BaseModel):
    hostel_id: int
    date: date
    water_litres: float = Field(..., ge=0)
    electricity_kwh: float = Field(..., ge=0)
    gas_kg: float = Field(..., ge=0)

class ConsumptionUpdate(BaseModel):
    water_litres: Optional[float] = Field(None, ge=0)
    electricity_kwh: Optional[float] = Field(None, ge=0)
    gas_kg: Optional[float] = Field(None, ge=0)

class ConsumptionResponse(BaseModel):
    id: int
    hostel_id: int
    hostel_name: Optional[str] = None
    hostel_block: Optional[str] = None
    date: date
    student_count: Optional[int] = 0
    water_litres: float
    electricity_kwh: float
    gas_kg: float
    water_cost: float
    electricity_cost: float
    gas_cost: float
    total_cost: float
    water_per_student: Optional[float] = 0.0
    electricity_per_student: Optional[float] = 0.0
    gas_per_student: Optional[float] = 0.0

    class Config:
        from_attributes = True

# Alerts Schemas
class AlertResponse(BaseModel):
    id: int
    hostel_id: int
    hostel_name: Optional[str] = None
    hostel_block: Optional[str] = None
    resource_type: str
    severity: str
    actual_value: float
    expected_value: float
    difference_percentage: float
    description: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class AlertUpdate(BaseModel):
    status: str

class ConvertAlertToMaintenanceRequest(BaseModel):
    priority: Optional[str] = "High"
    assigned_to: Optional[str] = None
    notes: Optional[str] = None

# Predictions Schemas
class ForecastDay(BaseModel):
    day_number: int
    date: str
    day_name: str
    predicted_value: float
    predicted_cost: float
    unit: str

class ModelEvaluation(BaseModel):
    model_name: str
    r2_score: float
    mae: float
    rmse: float

class PredictionResponse(BaseModel):
    hostel_id: Optional[int] = None
    hostel_name: Optional[str] = "All Hostels (Institution Aggregate)"
    resource_type: str
    current_rate: float
    unit: str
    forecast: List[ForecastDay]
    total_predicted_consumption: float
    total_predicted_cost: float
    explainability: List[str]
    model_evaluations: List[ModelEvaluation]

# Maintenance Schemas
class MaintenanceCreate(BaseModel):
    hostel_id: int
    resource_type: str
    issue_type: str
    description: str
    priority: Optional[str] = "Medium"
    assigned_to: Optional[str] = None
    notes: Optional[str] = None

class MaintenanceUpdate(BaseModel):
    priority: Optional[str] = None
    assigned_to: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    resolved_at: Optional[datetime] = None

class MaintenanceResponse(BaseModel):
    id: int
    hostel_id: int
    hostel_name: Optional[str] = None
    hostel_block: Optional[str] = None
    resource_type: str
    issue_type: str
    description: str
    priority: str
    assigned_to: Optional[str] = None
    status: str
    created_at: datetime
    resolved_at: Optional[datetime] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True

# Recommendations Schemas
class RecommendationItem(BaseModel):
    id: str
    hostel_id: Optional[int] = None
    hostel_name: str
    category: str # Water, Electricity, Gas, Occupancy, General
    title: str
    description: str
    suggested_actions: List[str]
    estimated_monthly_savings: float
    impact_level: str # High, Medium, Low
    reasoning: str

# Settings Schemas
class UtilityRateResponse(BaseModel):
    id: int
    resource_type: str
    rate: float
    unit: str
    effective_from: datetime

    class Config:
        from_attributes = True

class UtilityRateUpdate(BaseModel):
    rate: float
