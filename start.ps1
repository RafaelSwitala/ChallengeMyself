# UTF-8 Fix für Umlaute
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "================================" -ForegroundColor Cyan
Write-Host "ChallengeMyself - Start Script" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Paths
$backendPath = Join-Path $PSScriptRoot "backend"
$frontendPath = Join-Path $PSScriptRoot "frontend"
$venvPath = Join-Path $backendPath "venv\Scripts\Activate.ps1"

# 0. ALLE Prozesse auf Ports 3000 & 5000 killen (BESTE LÖSUNG)
Write-Host "Cleaning up ports 3000 and 5000..." -ForegroundColor Yellow

foreach ($port in 3000,5000) {
    $pids = netstat -ano | Select-String ":$port" | ForEach-Object {
        ($_ -split "\s+")[-1]
    } | Sort-Object -Unique

    foreach ($pid in $pids) {
        if ($pid -match "^\d+$") {
            try {
                taskkill /PID $pid /F | Out-Null
                Write-Host "Killed PID $pid on port $port" -ForegroundColor DarkYellow
            } catch {}
        }
    }
}

Start-Sleep -Seconds 1

# 1. Virtual Environment prüfen
Write-Host ""
Write-Host "1. Checking backend environment..." -ForegroundColor Green

if (-not (Test-Path $venvPath)) {
    Write-Host "Virtual environment not found. Creating it..." -ForegroundColor Yellow
    Set-Location $backendPath
    python -m venv venv
    & $venvPath
    pip install -r requirements.txt
    Set-Location $PSScriptRoot
}

# 2. Backend starten (sichtbar!)
Write-Host ""
Write-Host "2. Starting Backend (Flask) on Port 5000..." -ForegroundColor Green

Start-Process powershell `
    -ArgumentList "-NoExit", "-Command", "Set-Location '$backendPath'; & '$venvPath'; python run_server.py"

# 3. Frontend starten (sichtbar!)
Write-Host ""
Write-Host "3. Starting Frontend (React) on Port 3000..." -ForegroundColor Green

Start-Process powershell `
    -ArgumentList "-NoExit", "-Command", "Set-Location '$frontendPath'; npm start"

# 4. Warten
Write-Host ""
Write-Host "Warte 5 Sekunden, damit Services starten..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# 5. Browser öffnen
Write-Host ""
Write-Host "4. Opening app in browser at http://localhost:3000/..." -ForegroundColor Green
Start-Process "http://localhost:3000/"

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "App läuft:" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "Backend:  http://localhost:5000" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Schließe die geöffneten Terminal-Fenster zum Beenden" -ForegroundColor Yellow