#!/bin/bash

echo "🔄 FULL SAHAJAI REDEPLOY"

./redeploy_frontend.sh
./restart_backend.sh

echo "⚠️ If tunnel is required, run:"
echo "   ./restart_tunnel.sh"

echo "✅ Redeploy complete"
