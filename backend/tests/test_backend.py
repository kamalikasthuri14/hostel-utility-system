import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "Online"

def test_login_success():
    response = client.post(
        "/api/auth/login",
        json={"email": "admin@hostel.edu", "password": "Admin@123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["role"] == "admin"
    assert data["user"]["email"] == "admin@hostel.edu"

def test_login_invalid_password():
    response = client.post(
        "/api/auth/login",
        json={"email": "admin@hostel.edu", "password": "WrongPassword"}
    )
    assert response.status_code == 401

def test_dashboard_summary():
    auth_resp = client.post(
        "/api/auth/login",
        json={"email": "admin@hostel.edu", "password": "Admin@123"}
    )
    token = auth_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/dashboard/summary", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert data["summary"]["total_hostel_blocks"] == 8
    assert data["summary"]["total_students"] > 1000
    assert "efficiency_score" in data["summary"]

def test_hostels_list():
    auth_resp = client.post(
        "/api/auth/login",
        json={"email": "admin@hostel.edu", "password": "Admin@123"}
    )
    token = auth_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/hostels", headers=headers)
    assert response.status_code == 200
    hostels = response.json()
    assert len(hostels) == 8
    assert any(h["block"] == "Block A" for h in hostels)

def test_analytics_water_and_electricity():
    auth_resp = client.post(
        "/api/auth/login",
        json={"email": "admin@hostel.edu", "password": "Admin@123"}
    )
    token = auth_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    w_resp = client.get("/api/analytics/water?days=30", headers=headers)
    assert w_resp.status_code == 200
    assert "daily_trends" in w_resp.json()

    e_resp = client.get("/api/analytics/electricity?days=30", headers=headers)
    assert e_resp.status_code == 200
    assert "peak_breakdown" in e_resp.json()

def test_predictions_forecast():
    auth_resp = client.post(
        "/api/auth/login",
        json={"email": "admin@hostel.edu", "password": "Admin@123"}
    )
    token = auth_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/predictions?resource_type=Electricity", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["forecast"]) == 7
    assert "model_evaluations" in data
    assert len(data["explainability"]) > 0

def test_alerts_and_maintenance():
    auth_resp = client.post(
        "/api/auth/login",
        json={"email": "admin@hostel.edu", "password": "Admin@123"}
    )
    token = auth_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    alerts_resp = client.get("/api/alerts", headers=headers)
    assert alerts_resp.status_code == 200
    alerts = alerts_resp.json()
    assert len(alerts) > 0

    first_alert = alerts[0]
    conv_resp = client.post(
        f"/api/alerts/{first_alert['id']}/convert-to-ticket",
        json={"priority": "High", "notes": "Automated verification ticket test"},
        headers=headers
    )
    assert conv_resp.status_code == 200
    assert "ticket_id" in conv_resp.json()

def test_reports_monthly():
    auth_resp = client.post(
        "/api/auth/login",
        json={"email": "admin@hostel.edu", "password": "Admin@123"}
    )
    token = auth_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/reports/monthly", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "potential_optimized_cost" in data
    assert "estimated_possible_savings" in data
    assert len(data["blocks"]) > 0
