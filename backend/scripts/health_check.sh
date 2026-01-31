#!/bin/bash

API_URL=${1:-http://localhost:8080}

echo "🔍 Checking SahajAI Backend Health..."
echo "📡 URL: $API_URL/health"
echo "----------------------------------"

curl -s "$API_URL/health" || {
  echo "❌ Backend is NOT reachable"
  exit 1
}

echo
echo "✅ Backend is healthy"
