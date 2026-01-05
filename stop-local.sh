#!/bin/bash

echo "🛑 Stopping Research Platform..."

# Kill backend and frontend processes
pkill -f "uvicorn app.main:app" || true
pkill -f "vite" || true

# Stop docker services
docker compose down

echo "✅ All services stopped"
