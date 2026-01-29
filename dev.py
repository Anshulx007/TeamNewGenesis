import subprocess
import sys
import os
import signal

processes = []

def start_backend():
    print("🚀 Starting Backend...")
    return subprocess.Popen(
        ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"],
        cwd="backend"
    )

def start_frontend():
    print("🎨 Starting Frontend...")
    return subprocess.Popen(
        ["npm", "run", "dev"],
        cwd="frontend"
    )

def cleanup(signum, frame):
    print("\n🛑 Shutting down all services...")
    for p in processes:
        try:
            p.terminate()
        except:
            pass
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    backend_proc = start_backend()
    frontend_proc = start_frontend()

    processes.append(backend_proc)
    processes.append(frontend_proc)

    print("\n✅ SahajAI Dev Environment Started")
    print("Backend: http://localhost:8080")
    print("Frontend: http://localhost:5173")
    print("Press CTRL+C to stop everything\n")

    # Wait for both
    backend_proc.wait()
    frontend_proc.wait()
