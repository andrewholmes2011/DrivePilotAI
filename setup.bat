@echo off
title DrivePilotAI Setup
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
  echo Python 3 was not found. Install Python 3.11 or newer from https://www.python.org/downloads/
  echo Make sure "Add Python to PATH" is checked.
  pause
  exit /b 1
)
py -m venv .venv
call .venv\Scripts\activate.bat
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
echo.
echo Setup complete. Starting DrivePilotAI...
py app\main.py
pause
