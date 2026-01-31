#!/usr/bin/env python3
"""
SahajAI Full Deployment Script
Handles: Backend restart → Tunnel setup → Frontend build → Netlify deploy
"""

import subprocess
import os
import re
import time
import logging
import sys

# ----------------------------
# Paths
# ----------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))

BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")
FRONTEND_ENV = os.path.join(FRONTEND_DIR, ".env")
FRONTEND_DIST = os.path.join(FRONTEND_DIR, "dist")
LOG_DIR = os.path.join(ROOT_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "full_deploy.log")
TUNNEL_LOG = os.path.join(LOG_DIR, "tunnel.log")

os.makedirs(LOG_DIR, exist_ok=True)

# ----------------------------
# Logging setup
# ----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE, mode="a")
    ]
)

logger = logging.getLogger("sahajai-deploy")

# ----------------------------
# Regex
# ----------------------------
URL_REGEX = re.compile(r"https://[-a-zA-Z0-9.]+\.trycloudflare\.com")


# ----------------------------
# Step 1: Restart Backend
# ----------------------------
def restart_backend():
    logger.info("=" * 60)
    logger.info("STEP 1: Restarting Backend")
    logger.info("=" * 60)

    # Kill existing backend
    logger.info("🔁 Stopping existing backend...")
    subprocess.run(
        ["pkill", "-f", "uvicorn app.main:app"],
        check=False
    )
    time.sleep(1)

    # Start new backend
    logger.info("🚀 Starting backend on port 8080...")
    proc = subprocess.Popen(
        ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"],
        cwd=BACKEND_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True
    )

    time.sleep(3)
    logger.info("✅ Backend started")
    return True


# ----------------------------
# Step 2: Start Cloudflare Tunnel
# ----------------------------
def start_tunnel():
    logger.info("=" * 60)
    logger.info("STEP 2: Starting Cloudflare Tunnel")
    logger.info("=" * 60)

    # Kill existing tunnel
    logger.info("Checking for existing tunnel...")
    subprocess.run(
        ["pkill", "-f", "cloudflared tunnel --url"],
        check=False
    )
    time.sleep(2)

    # Start tunnel with nohup
    logger.info("🌐 Starting tunnel with nohup...")
    subprocess.Popen(
        f"nohup cloudflared tunnel --url http://localhost:8080 > {TUNNEL_LOG} 2>&1 &",
        shell=True,
        start_new_session=True
    )

    # Wait and capture URL
    logger.info("⏳ Waiting for tunnel to initialize...")
    time.sleep(6)

    url = None
    if os.path.exists(TUNNEL_LOG):
        with open(TUNNEL_LOG, "r") as f:
            content = f.read()
            match = URL_REGEX.search(content)
            if match:
                url = match.group(0)
                logger.info(f"Last 30 lines of tunnel log:\n{chr(10).join(content.split(chr(10))[-30:])}")

    if not url:
        logger.error("❌ Failed to get tunnel URL")
        return None

    logger.info(f"🔗 Tunnel URL: {url}")
    logger.info("✅ Tunnel started and running in background")
    
    return url


# ----------------------------
# Step 3: Update Frontend .env
# ----------------------------
def update_frontend_env(tunnel_url):
    logger.info("=" * 60)
    logger.info("STEP 3: Updating Frontend .env")
    logger.info("=" * 60)

    lines = []
    if os.path.exists(FRONTEND_ENV):
        with open(FRONTEND_ENV, "r") as f:
            lines = f.readlines()

    found = False
    for i, line in enumerate(lines):
        if line.startswith("VITE_BACKEND_URL="):
            lines[i] = f"VITE_BACKEND_URL={tunnel_url}\n"
            found = True
            break

    if not found:
        lines.append(f"VITE_BACKEND_URL={tunnel_url}\n")

    with open(FRONTEND_ENV, "w") as f:
        f.writelines(lines)

    logger.info(f"✏️ Updated .env with tunnel URL: {tunnel_url}")
    logger.info("✅ Frontend .env updated")
    return True


# ----------------------------
# Step 4: Build Frontend
# ----------------------------
def build_frontend():
    logger.info("=" * 60)
    logger.info("STEP 4: Building Frontend")
    logger.info("=" * 60)

    logger.info("📦 Running npm build...")
    result = subprocess.run(
        ["npm", "run", "build"],
        cwd=FRONTEND_DIR,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        logger.error(f"❌ Build failed:\n{result.stderr}")
        return False

    logger.info(result.stdout)
    logger.info("✅ Frontend built successfully")
    
    if os.path.exists(FRONTEND_DIST):
        logger.info(f"📁 Build output: {FRONTEND_DIST}")
    
    return True


# ----------------------------
# Step 5: Deploy to Netlify
# ----------------------------
def deploy_netlify():
    logger.info("=" * 60)
    logger.info("STEP 5: Deploying to Netlify")
    logger.info("=" * 60)

    logger.info("🌍 Deploying with Netlify CLI...")
    result = subprocess.run(
        ["netlify", "deploy", "--prod", "--dir=dist"],
        cwd=FRONTEND_DIR,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        logger.error(f"❌ Netlify deploy failed:\n{result.stderr}")
        return False

    # Parse output for URL
    output = result.stdout
    logger.info(output)
    
    # Extract production URL
    if "Deployed to production URL:" in output:
        lines = output.split("\n")
        for i, line in enumerate(lines):
            if "Deployed to production URL:" in line and i + 1 < len(lines):
                prod_url = lines[i + 1].strip()
                logger.info(f"🚀 Production URL: {prod_url}")
    
    logger.info("✅ Netlify deployment complete")
    return True


# ----------------------------
# Test Backend
# ----------------------------
def test_backend(tunnel_url):
    logger.info("=" * 60)
    logger.info("STEP 6: Testing Backend")
    logger.info("=" * 60)

    logger.info(f"🧪 Testing health endpoint: {tunnel_url}/health")
    
    try:
        result = subprocess.run(
            ["curl", "-s", f"{tunnel_url}/health"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0 and "ok" in result.stdout:
            logger.info(f"✅ Backend health check passed")
            return True
        else:
            logger.warning(f"⚠️ Health check response: {result.stdout}")
            return False
    except Exception as e:
        logger.warning(f"⚠️ Health check failed: {e}")
        return False


# ----------------------------
# Main Flow
# ----------------------------
def main():
    logger.info("\n")
    logger.info("╔" + "=" * 58 + "╗")
    logger.info("║" + " " * 58 + "║")
    logger.info("║" + "  🚀 SAHAJAI FULL DEPLOYMENT STARTED  ".center(58) + "║")
    logger.info("║" + " " * 58 + "║")
    logger.info("╚" + "=" * 58 + "╝")
    logger.info("\n")

    try:
        # Step 1: Backend
        if not restart_backend():
            raise Exception("Backend restart failed")

        # Step 2: Tunnel
        tunnel_url = start_tunnel()
        if not tunnel_url:
            raise Exception("Tunnel startup failed")

        # Step 3: Update env
        if not update_frontend_env(tunnel_url):
            raise Exception("Frontend .env update failed")

        # Step 4: Build
        if not build_frontend():
            raise Exception("Frontend build failed")

        # Step 5: Deploy
        if not deploy_netlify():
            raise Exception("Netlify deployment failed")

        # Step 6: Test
        test_backend(tunnel_url)

        # Success summary
        logger.info("\n")
        logger.info("╔" + "=" * 58 + "╗")
        logger.info("║" + " " * 58 + "║")
        logger.info("║" + "  ✅ DEPLOYMENT SUCCESSFUL  ".center(58) + "║")
        logger.info("║" + " " * 58 + "║")
        logger.info("╚" + "=" * 58 + "╝")
        logger.info("\n")
        
        logger.info("📊 Deployment Summary:")
        logger.info(f"  • Backend:    ✅ Running on localhost:8080")
        logger.info(f"  • Tunnel:     ✅ {tunnel_url}")
        logger.info(f"  • Frontend:   ✅ Built at {FRONTEND_DIST}")
        logger.info(f"  • Netlify:    ✅ Deployed")
        logger.info(f"  • Logs:       📁 {LOG_DIR}")
        logger.info("\n")

        return 0

    except Exception as e:
        logger.error("\n")
        logger.error("╔" + "=" * 58 + "╗")
        logger.error("║" + " " * 58 + "║")
        logger.error("║" + f"  ❌ DEPLOYMENT FAILED: {str(e)[:40]}".ljust(58) + "║")
        logger.error("║" + " " * 58 + "║")
        logger.error("╚" + "=" * 58 + "╝")
        logger.error("\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
