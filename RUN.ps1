# SPP Management System - PowerShell Start Script

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   SPP Management System - Starting...                  ║" -ForegroundColor Cyan
Write-Host "║   MINGGU 11: Modul Keuangan (SPP)                      ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Get script directory
$scriptPath = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
Set-Location $scriptPath

# Check if virtual environment exists
if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    Write-Host "❌ Error: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run: pip install -r requirements.txt" -ForegroundColor Yellow
    Read-Host "Press ENTER to exit"
    exit 1
}

Write-Host "✅ Virtual environment found" -ForegroundColor Green
Write-Host "✅ Starting Flask development server..." -ForegroundColor Green
Write-Host ""
Write-Host "📍 Server will start at: http://localhost:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press CTRL+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Run the Flask app
& .\.venv\Scripts\python.exe app.py
