# ChallengeMyself - Einzeiliger Start für Frontend und Backend
# Führe dieses Skript aus: .\start.ps1

Write-Host "================================" -ForegroundColor Cyan
Write-Host "ChallengeMyself - Start Script" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Backend Path
$backendPath = Join-Path $PSScriptRoot "backend"

# Frontend Path
$frontendPath = Join-Path $PSScriptRoot "frontend"

# 1. Backend venv aktivieren und starten
Write-Host "1️⃣  Starte Backend (Flask) auf Port 5000..." -ForegroundColor Green
$venvPath = Join-Path $backendPath "venv\Scripts\Activate.ps1"

if (-not (Test-Path $venvPath)) {
    Write-Host "⚠️  Virtuelle Umgebung nicht gefunden. Erstelle sie..." -ForegroundColor Yellow
    Set-Location $backendPath
    python -m venv venv
    & $venvPath
    pip install -r requirements.txt
    Set-Location $PSScriptRoot
}

# Backend im Hintergrund starten (versteckt)
$backendProcess = Start-Process -FilePath "powershell" `
    -ArgumentList "-NoExit", "-Command", "Set-Location '$backendPath'; & '$venvPath'; python run_server.py" `
    -PassThru `
    -WindowStyle Hidden

Write-Host "Backend-PID: $($backendProcess.Id)" -ForegroundColor Green

# 2. Frontend starten (auch im Hintergrund)
Write-Host "2️⃣  Starte Frontend (React) auf Port 3000..." -ForegroundColor Green
$frontendProcess = Start-Process -FilePath "powershell" `
    -ArgumentList "-NoExit", "-Command", "Set-Location '$frontendPath'; npm start" `
    -PassThru `
    -WindowStyle Hidden

Write-Host "Frontend-PID: $($frontendProcess.Id)" -ForegroundColor Green

# 3. Warte, damit beide starten
Write-Host ""
Write-Host "Warte 5 Sekunden, damit beide Services initialisiert..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# 4. Öffne App im Browser (React auf Port 3000)
Write-Host ""
Write-Host "3️⃣  Öffne App im Browser unter http://localhost:3000/..." -ForegroundColor Green
Start-Process "http://localhost:3000/"

Write-Host ""
Write-Host "✅ App lädt! Backend auf http://localhost:5000, Frontend auf http://localhost:3000" -ForegroundColor Cyan
Write-Host "   Drücke STRG+C zum Beenden." -ForegroundColor Cyan

# Warte auf Benutzer-Exit (STRG+C)
while ($true) {
    Start-Sleep -Seconds 60
}
