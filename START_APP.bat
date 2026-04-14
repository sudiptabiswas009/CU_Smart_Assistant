@echo off
title CU Smart Assistant
color 0A
echo.
echo  ============================================
echo    CU Smart Assistant - STARTING UP
echo  ============================================
echo.

cd /d "%~dp0"

echo  [Step 1] Checking for Python...
where python >nul 2>&1
if errorlevel 1 (
    echo  ERROR: Python not found in PATH!
    echo  Please install Python from https://python.org
    echo  Make sure to check "Add Python to PATH" during install.
    pause
    exit /b
)
python --version

echo.
echo  [Step 2] Installing required packages (may take a moment)...
.venv\Scripts\pip install flask google-generativeai python-dotenv --quiet 2>&1
if errorlevel 1 (
    echo  Venv pip failed, trying system pip...
    pip install flask google-generativeai python-dotenv --quiet 2>&1
)

echo.
echo  [Step 3] Starting Flask server on port 8080...
echo.
echo  ============================================
echo    Open browser to: http://127.0.0.1:8080
echo    Keep this window open while using the app!
echo    Press CTRL+C to stop.
echo  ============================================
echo.

.venv\Scripts\python app.py
if errorlevel 1 (
    echo.
    echo  Venv Python failed. Trying system Python...
    python app.py
)

echo.
echo  Server has stopped.
pause
