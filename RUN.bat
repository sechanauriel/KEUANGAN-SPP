@echo off
REM ============================================================
REM SPP Management System - Start Script for Windows
REM ============================================================

cd /d "%~dp0"

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║   SPP Management System - Starting...                  ║
echo ║   MINGGU 11: Modul Keuangan (SPP)                      ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Check if .venv exists
if not exist ".venv\Scripts\python.exe" (
    echo ❌ Error: Virtual environment not found!
    echo Please run: pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo ✅ Virtual environment found
echo ✅ Starting Flask development server...
echo.
echo 📍 Server will start at: http://localhost:5000
echo.
echo Press CTRL+C to stop the server
echo.

REM Run the Flask app
.\.venv\Scripts\python.exe app.py

pause
