#!/usr/bin/env python3
"""
SahajAI Deployment Status Checker
Shows current status of all services
"""

import subprocess
import os
import re

# Colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))
LOG_DIR = os.path.join(ROOT_DIR, "logs")
TUNNEL_LOG = os.path.join(LOG_DIR, "tunnel.log")
FRONTEND_ENV = os.path.join(ROOT_DIR, "frontend", ".env")

def get_status(name, cmd, grep_for=None):
    """Check if a process is running"""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )
    
    if grep_for and grep_for not in result.stdout:
        return False, None
    
    if result.returncode == 0:
        return True, result.stdout.strip()
    return False, result.stderr.strip()

def check_backend():
    print(f"\n{BLUE}Backend Status:{RESET}")
    running, output = get_status("Backend", "lsof -i :8080 | grep uvicorn")
    if running:
        print(f"  {GREEN}✅ Running on port 8080{RESET}")
        return True
    else:
        print(f"  {RED}❌ Not running{RESET}")
        return False

def check_tunnel():
    print(f"\n{BLUE}Tunnel Status:{RESET}")
    running, pid = get_status("Tunnel", "pgrep -f 'cloudflared tunnel'")
    if running:
        print(f"  {GREEN}✅ Running (PID: {pid.split()[0]}){RESET}")
        
        # Get tunnel URL from log
        if os.path.exists(TUNNEL_LOG):
            with open(TUNNEL_LOG, "r") as f:
                content = f.read()
                url_match = re.search(r"https://[-a-zA-Z0-9.]+\.trycloudflare\.com", content)
                if url_match:
                    url = url_match.group(0)
                    print(f"  🔗 URL: {YELLOW}{url}{RESET}")
                    return True, url
        return True, None
    else:
        print(f"  {RED}❌ Not running{RESET}")
        return False, None

def check_frontend_env():
    print(f"\n{BLUE}Frontend Configuration:{RESET}")
    if os.path.exists(FRONTEND_ENV):
        with open(FRONTEND_ENV, "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("VITE_BACKEND_URL="):
                    url = line.split("=", 1)[1].strip()
                    print(f"  🎨 Backend URL: {YELLOW}{url}{RESET}")
                    
                    # Test if reachable
                    result = subprocess.run(
                        f"curl -s -m 3 {url}/health",
                        shell=True,
                        capture_output=True,
                        text=True
                    )
                    if result.returncode == 0 and "ok" in result.stdout:
                        print(f"  {GREEN}✅ Backend reachable{RESET}")
                    else:
                        print(f"  {YELLOW}⚠️ Backend not reachable{RESET}")
                    return
    print(f"  {RED}❌ .env not found{RESET}")

def check_netlify():
    print(f"\n{BLUE}Netlify Status:{RESET}")
    print(f"  🌍 Frontend: {YELLOW}https://chimerical-ganache-a75468.netlify.app{RESET}")

def show_logs():
    print(f"\n{BLUE}Recent Logs:{RESET}")
    
    full_deploy_log = os.path.join(LOG_DIR, "full_deploy.log")
    if os.path.exists(full_deploy_log):
        print(f"\n  📄 Last 10 lines from full_deploy.log:")
        result = subprocess.run(
            f"tail -10 {full_deploy_log}",
            shell=True,
            capture_output=True,
            text=True
        )
        for line in result.stdout.split("\n")[-10:]:
            if line.strip():
                print(f"    {line}")

def main():
    print(f"\n{BOLD}{BLUE}╔════════════════════════════════════════╗{RESET}")
    print(f"{BOLD}{BLUE}║  SahajAI Deployment Status              ║{RESET}")
    print(f"{BOLD}{BLUE}╚════════════════════════════════════════╝{RESET}")
    
    backend_ok = check_backend()
    tunnel_ok, tunnel_url = check_tunnel()
    check_frontend_env()
    check_netlify()
    show_logs()
    
    print(f"\n{BLUE}Summary:{RESET}")
    print(f"  Backend:  {'✅' if backend_ok else '❌'}")
    print(f"  Tunnel:   {'✅' if tunnel_ok else '❌'}")
    print(f"  Frontend: {'✅' if os.path.exists(FRONTEND_ENV) else '❌'}")
    
    print(f"\n{BLUE}Next Steps:{RESET}")
    if not backend_ok:
        print(f"  • Restart backend: {YELLOW}python3 restart.py{RESET}")
    if not tunnel_ok:
        print(f"  • Start tunnel: {YELLOW}python3 restart.py{RESET}")
    print(f"  • Full deploy: {YELLOW}python3 full_deploy.py{RESET}")
    print(f"  • View app: {YELLOW}https://chimerical-ganache-a75468.netlify.app{RESET}")
    print()

if __name__ == "__main__":
    main()
