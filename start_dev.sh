#!/bin/bash

echo "🚀 Starting Youth Poll Development Environment..."

# Kill any existing processes
echo "🧹 Cleaning up existing processes..."
pkill -f uvicorn 2>/dev/null
pkill -f "npm run dev" 2>/dev/null

# Wait a moment for processes to clean up
sleep 2

# Start backend
echo "🔧 Starting backend server..."
cd backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start frontend
echo "🎨 Starting frontend server..."
cd ../youth-poll-frontend
npm run dev &
FRONTEND_PID=$!

echo "✅ Development environment started!"
echo "📱 Frontend: http://localhost:3001"
echo "🔧 Backend: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for user to stop
wait
