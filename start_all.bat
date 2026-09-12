@echo off
title Hostel Utility Optimization - Launcher
echo ========================================================
echo Launching Hostel Utility Optimization System
echo ========================================================
echo Starting Backend in a new window...
start "Hostel Backend API" cmd /k "cd /d %~dp0backend && python -m uvicorn app.main:app --reload --port 8000"

echo Starting Frontend in a new window...
start "Hostel Frontend UI" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ========================================================
echo Both servers launched!
echo - Frontend: http://localhost:5173
echo - Backend Docs: http://127.0.0.1:8000/docs
echo ========================================================
timeout /t 5
