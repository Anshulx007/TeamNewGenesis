import subprocess
import os
import signal
import time

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")


def run(cmd, cwd=None):
    print(f"▶️ Running: {' '.join(cmd)}")
    subprocess.run(cmd, cwd=cwd, check=True)


def redeploy_frontend():
    print("\n🌍 Redeploying Frontend")

    run(["npm", "install"], cwd=FRONTEND_DIR)
    run(["npm", "run", "build"], cwd=FRONTEND_DIR)
    run(["netlify", "deploy", "--prod", "--dir=dist"], cwd=FRONTEND_DIR)

    print("✅ Frontend redeployed")


def restart_backend():
    print("\n🔁 Restarting Backend")

    # Kill existing uvicorn process if running
    subprocess.run(
        ["pkill", "-f", "uvicorn app.main:app"],
        check=False
    )

    time.sleep(1)

    subprocess.Popen(
        ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"],
        cwd=BACKEND_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True
    )

    time.sleep(2)
    print("✅ Backend restarted")


if __name__ == "__main__":
    print("🔄 SAHAJAI REDEPLOY STARTED")

    redeploy_frontend()
    restart_backend()

    print("\n⚠️ Cloudflare tunnel NOT restarted (URL remains stable)")
    print("✅ Redeploy complete")
