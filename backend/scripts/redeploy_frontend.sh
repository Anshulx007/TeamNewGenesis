#!/bin/bash
set -e

echo "🚀 Redeploying SahajAI Frontend"

# go to frontend from backend/scripts
cd ../../frontend || exit 1

echo "📦 Installing dependencies"
npm install

echo "🏗️ Building frontend"
npm run build

echo "🌍 Deploying to Netlify"
netlify deploy --prod --dir=dist

echo "✅ Frontend redeployed successfully"
