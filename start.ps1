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

# Backend im Hintergrund starten
$backendProcess = Start-Process -FilePath "powershell" `
    -ArgumentList "-NoExit", "-Command", "Set-Location '$backendPath'; & '$venvPath'; python app.py" `
    -PassThru `
    -WindowStyle Normal

Write-Host "Backend-PID: $($backendProcess.Id)" -ForegroundColor Green

# 2. Warte, damit Backend startet
Write-Host ""
Write-Host "Warte 3 Sekunden, damit Backend initialisiert..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# 3. Öffne App im Browser (nur Flask auf Port 5000)
Write-Host ""
Write-Host "2️⃣  Öffne App im Browser unter http://localhost:5000/..." -ForegroundColor Green
Start-Process "http://localhost:5000/"

Write-Host ""
Write-Host "✅ App lädt! Drücke STRG+C zum Beenden." -ForegroundColor Cyan

# Warte auf Benutzer-Exit (STRG+C)
while ($true) {
    Start-Sleep -Seconds 60
}
