import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any
from sklearn.ensemble import IsolationForest
from sqlalchemy.orm import Session

from app.database.models import UtilityConsumption, Alert, Hostel
from app.ml.data_preprocessing import load_consumption_dataframe

def run_anomaly_detection(db: Session) -> List[Dict[str, Any]]:
    """
    Runs Isolation Forest and Rolling Z-Score anomaly detection across all hostel blocks.
    Identifies abnormal spikes/drops and automatically records active alerts.
    """
    hostels = db.query(Hostel).all()
    detected_alerts = []

    for h in hostels:
        df = load_consumption_dataframe(db, hostel_id=h.id)
        if df.empty or len(df) < 7:
            continue

        resources = [
            ("Water", "water_litres", "L", 25.0, 50.0, 75.0),
            ("Electricity", "electricity_kwh", "kWh", 20.0, 40.0, 65.0),
            ("Gas", "gas_kg", "kg", 25.0, 45.0, 70.0)
        ]

        for res_name, col_name, unit, med_thresh, high_thresh, crit_thresh in resources:
            # Features for Isolation Forest
            feat_df = df[["student_count", "occupancy_pct", col_name]].copy()
            feat_df["per_student"] = feat_df[col_name] / np.maximum(feat_df["student_count"], 1)

            # Fit Isolation Forest (contamination ~5%)
            iso = IsolationForest(contamination=0.06, random_state=42)
            iso.fit(feat_df)
            iso_scores = iso.predict(feat_df) # -1 is anomaly, 1 is normal

            # Calculate rolling 14-day expected baseline
            df["expected"] = df[col_name].rolling(window=14, min_periods=3).median().shift(1)
            df["expected"] = df["expected"].fillna(df[col_name].mean())

            # Evaluate recent 14 records for anomalies
            recent_df = df.tail(14).copy()
            recent_scores = iso_scores[-14:]

            for idx, (_, row) in enumerate(recent_df.iterrows()):
                is_iso_anomaly = (recent_scores[idx] == -1)
                actual = float(row[col_name])
                expected = max(1.0, float(row["expected"]))
                diff_pct = ((actual - expected) / expected) * 100

                # If significant positive surge detected
                if diff_pct > 15.0 or (is_iso_anomaly and diff_pct > 10.0):
                    if diff_pct >= crit_thresh:
                        severity = "Critical"
                    elif diff_pct >= high_thresh:
                        severity = "High"
                    elif diff_pct >= med_thresh:
                        severity = "Medium"
                    else:
                        severity = "Low"

                    rec_date = row["date"].date() if hasattr(row["date"], "date") else row["date"]
                    desc = f"{h.name} ({h.block}) {res_name.lower()} usage of {int(actual):,} {unit} is {round(diff_pct, 1)}% above expected baseline ({int(expected):,} {unit})."

                    # Check if alert already logged for this hostel, resource, and date
                    existing = db.query(Alert).filter(
                        Alert.hostel_id == h.id,
                        Alert.resource_type == res_name,
                        Alert.description.like(f"%{h.block}%{res_name.lower()}%")
                    ).first()

                    if not existing:
                        new_alert = Alert(
                            hostel_id=h.id,
                            resource_type=res_name,
                            severity=severity,
                            actual_value=round(actual, 2),
                            expected_value=round(expected, 2),
                            difference_percentage=round(diff_pct, 1),
                            description=desc,
                            status="Active",
                            created_at=datetime.utcnow()
                        )
                        db.add(new_alert)
                        db.commit()
                        db.refresh(new_alert)

                    detected_alerts.append({
                        "hostel_id": h.id,
                        "hostel_name": h.name,
                        "hostel_block": h.block,
                        "resource_type": res_name,
                        "severity": severity,
                        "actual_value": actual,
                        "expected_value": expected,
                        "difference_percentage": round(diff_pct, 1),
                        "description": desc,
                        "date": str(rec_date)
                    })

    return detected_alerts
