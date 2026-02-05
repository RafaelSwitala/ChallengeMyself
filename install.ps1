# ChallengeMyself Installation Script
# This script sets up the Python virtual environment and installs all dependencies

param(
    [string]$pythonVersion = "3.10"
)

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "ChallengeMyself - Installation Script" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonCheck = python --version 2>&1
    Write-Host "Found Python: $pythonCheck" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.10+ from https://www.python.org/" -ForegroundColor Red
    exit 1
}

# Check if Node.js/npm is installed
try {
    $npmCheck = npm --version 2>&1
    Write-Host "Found npm: version $npmCheck" -ForegroundColor Green
} catch {
    Write-Host "WARNING: npm is not installed. Frontend setup will be skipped." -ForegroundColor Yellow
    $skipFrontend = $true
}

Write-Host ""
Write-Host "Step 1: Creating Python virtual environment..." -ForegroundColor Yellow

if (Test-Path "venv") {
    Write-Host "Virtual environment already exists. Skipping creation." -ForegroundColor Cyan
} else {
    try {
        python -m venv venv
        Write-Host "Virtual environment created successfully" -ForegroundColor Green
    } catch {
        Write-Host "ERROR: Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "Step 2: Activating virtual environment..." -ForegroundColor Yellow

try {
    & ".\venv\Scripts\Activate.ps1"
    Write-Host "Virtual environment activated" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Failed to activate virtual environment" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Step 3: Installing Python dependencies..." -ForegroundColor Yellow

if (Test-Path "backend/requirements.txt") {
    try {
        pip install -r backend/requirements.txt --upgrade
        Write-Host "Python dependencies installed successfully" -ForegroundColor Green
    } catch {
        Write-Host "ERROR: Failed to install Python dependencies" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "ERROR: backend/requirements.txt not found" -ForegroundColor Red
    exit 1
}

if (-not $skipFrontend) {
    Write-Host ""
    Write-Host "Step 4: Installing Node.js dependencies..." -ForegroundColor Yellow
    
    if (Test-Path "frontend") {
        try {
            Push-Location frontend
            npm install
            Pop-Location
            Write-Host "Node.js dependencies installed successfully" -ForegroundColor Green
        } catch {
            Write-Host "ERROR: Failed to install Node.js dependencies" -ForegroundColor Red
            Pop-Location
            exit 1
        }
    } else {
        Write-Host "WARNING: frontend directory not found. Skipping Node.js setup." -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "Installation completed successfully!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "To start the application, run:" -ForegroundColor Cyan
Write-Host "  .\start.ps1" -ForegroundColor Yellow
Write-Host ""
