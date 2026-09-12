from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.connection import engine, SessionLocal, Base
from app.database.models import User
from app.database.seed import seed_database
from app.api import (
    auth, dashboard, hostels, occupancy, consumption,
    analytics, anomalies, predictions, recommendations,
    alerts, maintenance, reports, settings
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Hostel Utility Optimization & Predictive Resource Management API",
    description="Backend API for high-density student hostel utility optimization, predictive forecasting, anomaly detection, and maintenance workflows.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_db_check():
    """Ensure database has seed records and pre-trained ML models on first startup"""
    db = SessionLocal()
    try:
        if db.query(User).count() == 0:
            print("Database is empty. Running initial institutional seed...")
            seed_database()
            print("Initial seed complete!")
    except Exception as e:
        print("Startup database check:", e)
    finally:
        db.close()

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(hostels.router)
app.include_router(occupancy.router)
app.include_router(consumption.router)
app.include_router(analytics.router)
app.include_router(anomalies.router)
app.include_router(predictions.router)
app.include_router(recommendations.router)
app.include_router(alerts.router)
app.include_router(maintenance.router)
app.include_router(reports.router)
app.include_router(settings.router)

@app.get("/")
def root():
    return {
        "system": "Automated Hostel Utility Optimization and Predictive Resource Management Dashboard",
        "status": "Online",
        "documentation": "/docs"
    }
