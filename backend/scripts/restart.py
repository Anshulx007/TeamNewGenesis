import subprocess
import os
import re
import time
import logging

# ----------------------------
# Paths
# ----------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))

BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
FRONTEND_ENV = os.path.join(ROOT_DIR, "frontend", ".env")
LOG_DIR = os.path.join(ROOT_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "restart.log")

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

logger = logging.getLogger("sahajai-restart")

# ----------------------------
# Helpers
# ----------------------------
TUNNEL_CMD = ["cloudflared", "tunnel", "--url", "http://localhost:8080"]
URL_REGEX = re.compile(r"https://[-a-zA-Z0-9.]+\.trycloudflare\.com")


def restart_backend():
    logger.info("🔁 Restarting backend")

    subprocess.run(
        ["pkill", "-f", "uvicorn app.main:app"],
        check=False
    )
    logger.info("Stopped existing backend (if any)")

    time.sleep(1)

    subprocess.Popen(
        ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"],
        cwd=BACKEND_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True
    )

    time.sleep(2)
    logger.info("✅ Backend started")


def update_env(url: str):
    lines = []
    found = False

    if os.path.exists(FRONTEND_ENV):
        with open(FRONTEND_ENV, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        if line.startswith("VITE_BACKEND_URL="):
            lines[i] = f"VITE_BACKEND_URL={url}\n"
            found = True

    if not found:
        lines.append(f"VITE_BACKEND_URL={url}\n")

    with open(FRONTEND_ENV, "w") as f:
        f.writelines(lines)

    logger.info("✏️ Updated frontend/.env with backend URL")


def start_cloudflare_tunnel():
    logger.info("🌐 Starting Cloudflare tunnel")

    # Check if tunnel is already running
    result = subprocess.run(
        ["pgrep", "-f", "cloudflared tunnel --url"],
        capture_output=True
    )
    
    if result.returncode == 0:
        logger.info("⚠️ Tunnel already running, killing it first...")
        subprocess.run(["pkill", "-f", "cloudflared tunnel --url"], check=False)
        time.sleep(2)

    # Start tunnel with nohup to keep it running persistently
    tunnel_log = os.path.join(LOG_DIR, "tunnel.log")
    
    logger.info(f"Starting tunnel with nohup (logs: {tunnel_log})")
    subprocess.Popen(
        f"nohup cloudflared tunnel --url http://localhost:8080 > {tunnel_log} 2>&1 &",
        shell=True,
        start_new_session=True
    )
    
    # Wait for tunnel to start and capture URL
    time.sleep(5)
    
    url = None
    if os.path.exists(tunnel_log):
        with open(tunnel_log, "r") as f:
            content = f.read()
            match = URL_REGEX.search(content)
            if match:
                url = match.group(0)
                logger.info(content)

    if not url:
        logger.error("❌ Failed to capture Cloudflare URL from tunnel logs")
        return

    logger.info("🔗 Cloudflare Tunnel URL: %s", url)
    update_env(url)
    logger.info("✅ Tunnel started and running in background")


# ----------------------------
# Entry Point
# ----------------------------
if __name__ == "__main__":
    logger.info("========================================")
    logger.info("🔄 SAHAJAI FULL RESTART STARTED")
    logger.info("========================================")

    restart_backend()
    start_cloudflare_tunnel()
    
    logger.info("========================================")
    logger.info("✅ SAHAJAI RESTART COMPLETE")
    logger.info("========================================")
    logger.info("🌐 Tunnel is running in background")
    logger.info("📍 Check logs at: /workspaces/TeamNewGenesis/logs/")
    logger.info("========================================")
