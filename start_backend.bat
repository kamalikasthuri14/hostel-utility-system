@echo off
title Hostel Utility Optimization - Backend API Server
echo ========================================================
echo Starting FastAPI Backend Server on http://127.0.0.1:8000
echo Swagger API Docs: http://127.0.0.1:8000/docs
echo ========================================================
cd /d "%~dp0backend"
python -m uvicorn app.main:app --reload --port 8000
pause
