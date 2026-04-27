@echo off
title FoodExpress - Server Launcher
color 0A

echo.
echo  ==========================================
echo    FoodExpress Food Ordering System
echo  ==========================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python not found! Please install Python first.
    echo  Download: https://www.python.org/downloads/
    pause
    exit
)

:: Install backend dependencies if not installed
echo  [1/3] Checking backend dependencies...
cd /d "%~dp0backend"
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo  Installing dependencies...
    pip install -r requirements.txt
)
echo  [OK] Dependencies ready.

:: Check if DB is setup (setup_db.py)
echo.
echo  [2/3] Setting up database...
python setup_db.py
echo.

:: Start Backend in new window
echo  [3/3] Starting servers...
start "FoodExpress - Backend :8000" cmd /k "cd /d "%~dp0backend" && echo Backend starting on http://localhost:8000 && echo Press Ctrl+C to stop && uvicorn main:app --reload --host 0.0.0.0 --port 8000"

:: Wait for backend to start
timeout /t 3 /nobreak >nul

:: Start Frontend in new window
start "FoodExpress - Frontend :3000" cmd /k "cd /d "%~dp0frontend" && python -m http.server 3000"

:: Wait for frontend to start
timeout /t 2 /nobreak >nul

echo.
echo  ==========================================
echo   Both servers are running!
echo.
echo   Frontend  : http://localhost:3000
echo   Backend   : http://localhost:8000
echo   API Docs  : http://localhost:8000/docs
echo.
echo   Admin Login : admin@food.com / admin123
echo  ==========================================
echo.

:: Open browser
start http://localhost:3000

echo  Close the two server windows to stop the app.
echo.
pause
