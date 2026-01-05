#!/bin/bash
set -e

echo "🚀 Starting Research Platform locally..."

# Start docker services
echo "📦 Starting PostgreSQL, MinIO, Redis..."
docker compose up -d db minio redis

# Wait for PostgreSQL
echo "⏳ Waiting for database..."
sleep 5

# Setup backend
echo "🔧 Setting up backend..."
cd backend

# Copy local env
cp .env.local .env

# Run migrations
echo "📊 Running database migrations..."
/usr/bin/python3 -m alembic upgrade head

# Seed data
echo "🌱 Seeding database..."
/usr/bin/python3 app/db/seed.py

# Start backend in background
echo "🖥️  Starting backend server..."
/usr/bin/python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

cd ..

# Setup frontend
echo "🎨 Setting up frontend..."
cd frontend

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
  echo "📦 Installing frontend dependencies..."
  npm install
fi

# Start frontend
echo "🌐 Starting frontend dev server..."
npm run dev &
FRONTEND_PID=$!

cd ..

echo ""
echo "✅ Application is running!"
echo "   Backend:  http://localhost:8000/docs"
echo "   Frontend: http://localhost:5173"
echo ""
echo "Default users (password: ChangeMe!123):"
echo "  - admin@example.com (Admin)"
echo "  - hod@example.com (HOD)"
echo "  - supervisor@example.com (Supervisor)"
echo "  - student@example.com (Student)"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
