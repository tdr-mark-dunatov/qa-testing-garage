@echo off
REM 🏁 Webhook Pitstop - Development Script (Windows)

echo 🏁 Starting Webhook Pitstop Development Environment...

REM Check if Python dependencies are installed
if not exist "apps\api\poetry.lock" (
    echo 📦 Installing Python dependencies with Poetry...
    cd apps\api
    poetry install
    cd ..\..
)

REM Check if Node dependencies are installed
if not exist "apps\web\node_modules" (
    echo 📦 Installing Node dependencies...
    cd apps\web
    call npm install
    cd ..\..
)

echo 🚀 Starting API (port 8000) and Web (port 5173)...

REM Start both in new windows
start "Webhook Pitstop API" cmd /k "cd apps\api && poetry run uvicorn main:app --reload"
start "Webhook Pitstop Web" cmd /k "cd apps\web && npm run dev"

echo ✅ Both apps starting in separate windows
pause
