#!/bin/bash

# 🏁 Webhook Pitstop - Development Script
# Runs both API and Web apps concurrently

echo "🏁 Starting Webhook Pitstop Development Environment..."

# Check if backend dependencies are installed
if [ ! -f "apps/api/poetry.lock" ]; then
  echo "📦 Installing Python dependencies with Poetry..."
  cd apps/api
  poetry install
  cd ../..
fi

# Check if frontend dependencies are installed
if [ ! -d "apps/web/node_modules" ]; then
  echo "📦 Installing Node dependencies..."
  cd apps/web
  npm install
  cd ../..
fi

# Run both apps concurrently
echo "🚀 Starting API (port 8000) and Web (port 5173)..."

trap 'kill 0' SIGINT

# Start API
(cd apps/api && poetry run uvicorn main:app --reload) &

# Start Web
(cd apps/web && npm run dev) &

wait
