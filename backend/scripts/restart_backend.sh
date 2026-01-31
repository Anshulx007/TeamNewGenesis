#!/bin/bash

echo "🔁 Restarting SahajAI Backend"

# Kill existing backend if running
pkill -f "uvicorn app.main:app" || true

sleep 1

cd .. || exit 1

echo "🚀 Starting backend"
uvicorn app.main:app --host 0.0.0.0 --port 8080 &

sleep 2

echo "✅ Backend restarted"
