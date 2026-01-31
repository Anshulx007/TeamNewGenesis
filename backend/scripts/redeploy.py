import subprocess
import os
import logging
from datetime import datetime

# ----------------------------
# Paths
# ----------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))
LOG_DIR = os.path.join(ROOT_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "redeploy.log")

REDEPLOY_SCRIPT = os.path.join(SCRIPT_DIR, "redeploy.sh")

# Ensure logs directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# ----------------------------
# Logging setup
# ----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),              # console
        logging.FileHandler(LOG_FILE, mode="a")  # file
    ]
)

logger = logging.getLogger("sahajai-redeploy")


def run_redeploy():
    if not os.path.exists(REDEPLOY_SCRIPT):
        logger.error("❌ redeploy.sh not found at %s", REDEPLOY_SCRIPT)
        return

    logger.info("🔄 Starting redeploy via redeploy.sh")

    process = subprocess.Popen(
        ["bash", REDEPLOY_SCRIPT],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    # Stream output line-by-line into logs
    for line in process.stdout:
        logger.info(line.rstrip())

    process.wait()

    if process.returncode == 0:
        logger.info("✅ Redeploy completed successfully")
    else:
        logger.error("❌ Redeploy failed with exit code %s", process.returncode)


if __name__ == "__main__":
    logger.info("========================================")
    logger.info("SAHAJAI REDEPLOY RUN STARTED")
    logger.info("========================================")

    run_redeploy()

    logger.info("========================================")
    logger.info("SAHAJAI REDEPLOY RUN FINISHED")
    logger.info("========================================")
