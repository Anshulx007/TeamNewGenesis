#!/bin/bash

API_URL=${1:-http://localhost:8080}

echo "🚀 SahajAI Demo Test"
echo "🌐 API: $API_URL"
echo "----------------------------------"

echo "➡️ Test 1: Greeting"
curl -s -X POST "$API_URL/api/chat/" \
  -H "Content-Type: application/json" \
  -d '{"message":"hi","language":"en"}'
echo -e "\n----------------------------------"

echo "➡️ Test 2: Aadhaar documents"
curl -s -X POST "$API_URL/api/chat/" \
  -H "Content-Type: application/json" \
  -d '{"message":"what documents are required for aadhaar","language":"en"}'
echo -e "\n----------------------------------"

echo "➡️ Test 3: PM Awas Yojana"
curl -s -X POST "$API_URL/api/chat/" \
  -H "Content-Type: application/json" \
  -d '{"message":"what is pm awas yojana","language":"en"}'
echo -e "\n----------------------------------"

echo "✅ Demo test completed"
