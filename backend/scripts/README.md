# SahajAI Deployment Scripts

This directory contains automated deployment scripts for SahajAI.

## Available Scripts

### 🚀 `full_deploy.py` - Complete Automated Deployment (RECOMMENDED)

**What it does:**
1. Restarts the backend (FastAPI on port 8080)
2. Starts Cloudflare tunnel (for online access)
3. Updates frontend `.env` with tunnel URL
4. Builds the frontend
5. Deploys to Netlify
6. Tests the backend through the tunnel

**Usage:**
```bash
python3 full_deploy.py
# or
./deploy.sh
```

**Output:**
- Logs: `/logs/full_deploy.log`
- Tunnel logs: `/logs/tunnel.log`

---

### 🔄 `restart.py` - Backend + Tunnel Only

Restarts backend and starts tunnel (no frontend deploy).

**Usage:**
```bash
python3 restart.py
```

**Output:**
- Logs: `/logs/restart.log`

---

### 🔁 `restart_backend.sh` - Backend Only

Just restarts the FastAPI backend.

**Usage:**
```bash
./restart_backend.sh
```

---

### 🌐 `start_tunnel_and_update_env.py` - Tunnel Only

Creates a Cloudflare tunnel and updates `.env`.

**Usage:**
```bash
python3 start_tunnel_and_update_env.py
```

---

### 📦 `redeploy.sh` - Full Redeploy (Legacy)

Runs `redeploy_frontend.sh` + `restart_backend.sh`.

**Usage:**
```bash
./redeploy.sh
```

---

### 🎨 `redeploy_frontend.sh` - Frontend Only

Installs dependencies, builds, and deploys to Netlify.

**Usage:**
```bash
./redeploy_frontend.sh
```

---

### 🧪 `demo_test.sh` - Run Demo Tests

Tests the backend with sample queries.

**Usage:**
```bash
./demo_test.sh http://localhost:8080
```

---

### 💊 `health_check.sh` - Backend Health Check

Checks if backend is running.

**Usage:**
```bash
./health_check.sh http://localhost:8080
```

---

## Quick Start

### For Development (Local Testing)
```bash
cd /workspaces/TeamNewGenesis
python3 dev.py  # Starts backend + frontend locally
```

### For Production Deployment
```bash
cd /workspaces/TeamNewGenesis/backend/scripts
python3 full_deploy.py
```

This will:
- ✅ Deploy backend
- ✅ Setup tunnel
- ✅ Deploy to Netlify
- ✅ Return tunnel URL and Netlify URL

---

## How It Works

### Tunnel Persistence
The tunnel is started with `nohup`, meaning it runs in the background even if the terminal closes. This is critical for production!

Check tunnel status:
```bash
ps aux | grep cloudflared
```

Kill tunnel if needed:
```bash
pkill -f "cloudflared tunnel"
```

### Environment Variables
- `VITE_BACKEND_URL`: Updated in `frontend/.env` with the tunnel URL
- This allows frontend to connect to backend through the internet

### Logs
All deployment activities are logged to:
- `/logs/full_deploy.log` - Full deployment log
- `/logs/tunnel.log` - Tunnel connection logs
- `/logs/restart.log` - Restart logs

---

## Troubleshooting

### Tunnel not connecting
```bash
# Check if tunnel is running
ps aux | grep cloudflared

# View tunnel logs
tail -f /workspaces/TeamNewGenesis/logs/tunnel.log

# Restart tunnel
python3 restart.py
```

### Frontend not connecting to backend
1. Check `.env` file has correct tunnel URL
2. Run `python3 full_deploy.py` to get fresh tunnel
3. Check browser console for errors
4. Test manually:
   ```bash
   curl https://YOUR-TUNNEL-URL/health
   ```

### Netlify deployment failed
```bash
# Make sure you're authenticated
netlify login

# Deploy manually
cd /workspaces/TeamNewGenesis/frontend
netlify deploy --prod --dir=dist
```

---

## File Descriptions

| File | Purpose | Uses |
|------|---------|------|
| `full_deploy.py` | Complete automated deployment | Python 3 |
| `restart.py` | Backend + tunnel restart | Python 3, subprocess |
| `deploy.sh` | Wrapper for full_deploy.py | Bash |
| `restart_backend.sh` | Backend restart | Bash, uvicorn |
| `redeploy_frontend.sh` | Frontend build + deploy | Bash, npm, netlify |
| `start_tunnel_and_update_env.py` | Tunnel setup | Python 3, cloudflared |
| `demo_test.sh` | API tests | Bash, curl |
| `health_check.sh` | Backend health check | Bash, curl |
| `redeploy.py` | Legacy full redeploy | Python 3, subprocess |
| `redeploy.sh` | Legacy wrapper | Bash |

---

## Requirements

Ensure these are installed:
- `python3` - For deployment scripts
- `npm` - For frontend building
- `netlify-cli` - For Netlify deployment
- `cloudflared` - For tunnel
- `uvicorn` - For backend
- `curl` - For testing

Install missing tools:
```bash
# cloudflared
curl -L --output cloudflared.tgz https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.tgz
tar -xzf cloudflared.tgz
sudo mv cloudflared /usr/bin/

# netlify
npm install -g netlify-cli

# uvicorn
pip install uvicorn fastapi
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  User (Internet)                         │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  Netlify (Frontend)   │
         │  chimerical-ganache   │
         └───────────┬───────────┘
                     │ (HTTPS)
                     ▼
         ┌───────────────────────┐
         │ Cloudflare Tunnel     │
         │ (trycloudflare.com)   │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  Backend (FastAPI)    │
         │  localhost:8080       │
         └───────────────────────┘
```

---

## Next Steps

1. **Test deployment**: Run `python3 full_deploy.py`
2. **Monitor logs**: `tail -f /logs/full_deploy.log`
3. **Check status**: Visit https://chimerical-ganache-a75468.netlify.app
4. **Test API**: Try sending a message in the web app

---

**Last Updated**: 2026-01-31
**Maintainer**: Team NewGenesis
