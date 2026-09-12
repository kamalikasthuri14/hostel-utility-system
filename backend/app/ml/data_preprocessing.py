import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database.models import UtilityConsumption, Occupancy, Hostel

def load_consumption_dataframe(db: Session, hostel_id: int = None) -> pd.DataFrame:
    query = db.query(
        UtilityConsumption.id,
        UtilityConsumption.hostel_id,
        UtilityConsumption.date,
        UtilityConsumption.water_litres,
        UtilityConsumption.electricity_kwh,
        UtilityConsumption.gas_kg,
        UtilityConsumption.water_cost,
        UtilityConsumption.electricity_cost,
        UtilityConsumption.gas_cost,
        UtilityConsumption.total_cost,
        Occupancy.student_count,
        Hostel.capacity,
        Hostel.name.label("hostel_name"),
        Hostel.block.label("hostel_block")
    ).join(
        Hostel, UtilityConsumption.hostel_id == Hostel.id
    ).outerjoin(
        Occupancy, (UtilityConsumption.hostel_id == Occupancy.hostel_id) & (UtilityConsumption.date == Occupancy.date)
    )

    if hostel_id:
        query = query.filter(UtilityConsumption.hostel_id == hostel_id)

    results = query.order_by(UtilityConsumption.date.asc()).all()
    if not results:
        return pd.DataFrame()

    df = pd.DataFrame([dict(r._mapping) for r in results])
    df["date"] = pd.to_datetime(df["date"])
    df["student_count"] = df["student_count"].fillna(df["capacity"] * 0.9).astype(float)
    df["occupancy_pct"] = (df["student_count"] / df["capacity"] * 100).clip(0, 100)

    # Per-student metrics
    df["water_per_student"] = df["water_litres"] / np.maximum(df["student_count"], 1)
    df["electricity_per_student"] = df["electricity_kwh"] / np.maximum(df["student_count"], 1)
    df["gas_per_student"] = df["gas_kg"] / np.maximum(df["student_count"], 1)

    return df

def create_ml_features(df: pd.DataFrame, target_col: str) -> (pd.DataFrame, pd.Series):
    if df.empty or len(df) < 14:
        return None, None

    df = df.copy().sort_values("date").reset_index(drop=True)

    # Calendar features
    df["day_of_week"] = df["date"].dt.dayofweek
    df["day_of_month"] = df["date"].dt.day
    df["month"] = df["date"].dt.month
    df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)

    # Rolling lag features for target column
    df["lag_1"] = df[target_col].shift(1)
    df["lag_2"] = df[target_col].shift(2)
    df["lag_7"] = df[target_col].shift(7)
    df["rolling_mean_7"] = df[target_col].shift(1).rolling(window=7, min_periods=1).mean()
    df["rolling_std_7"] = df[target_col].shift(1).rolling(window=7, min_periods=1).std().fillna(0)
    df["rolling_mean_14"] = df[target_col].shift(1).rolling(window=14, min_periods=1).mean()

    # Drop early rows with NaN lags
    clean_df = df.dropna(subset=["lag_7", "rolling_mean_7"]).reset_index(drop=True)
    if clean_df.empty:
        clean_df = df.bfill().ffill()

    feature_cols = [
        "student_count", "occupancy_pct", "day_of_week", "day_of_month",
        "month", "is_weekend", "lag_1", "lag_2", "lag_7", "rolling_mean_7",
        "rolling_std_7", "rolling_mean_14"
    ]

    X = clean_df[feature_cols]
    y = clean_df[target_col]
    return X, y
