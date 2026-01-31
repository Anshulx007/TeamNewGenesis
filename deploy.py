#!/usr/bin/env python3
"""
SahajAI Deploy - Quick launcher from project root
Run from: /workspaces/TeamNewGenesis/
Usage: python3 deploy.py [command]
"""

import subprocess
import sys
import os

SCRIPT_DIR = os.path.join(os.path.dirname(__file__), "backend/scripts")

def show_help():
    print("""
╔════════════════════════════════════════╗
║  SahajAI Quick Deploy                   ║
╚════════════════════════════════════════╝

Usage: python3 deploy.py [command]

Commands:
  full        Full deployment (default)
  restart     Restart backend + tunnel
  status      Show deployment status
  test        Run demo tests
  help        Show this help

Examples:
  python3 deploy.py              # Full deploy
  python3 deploy.py restart      # Just restart
  python3 deploy.py status       # Check status
  python3 deploy.py test         # Run tests
    """)

def run_command(script_name):
    script_path = os.path.join(SCRIPT_DIR, script_name)
    if not os.path.exists(script_path):
        print(f"❌ Script not found: {script_path}")
        return 1
    
    try:
        result = subprocess.run([f"python3", script_path], cwd=SCRIPT_DIR)
        return result.returncode
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

def main():
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
    else:
        command = "full"
    
    if command == "help" or command == "-h" or command == "--help":
        show_help()
        return 0
    elif command == "full":
        return run_command("full_deploy.py")
    elif command == "restart":
        return run_command("restart.py")
    elif command == "status":
        return run_command("status.py")
    elif command == "test":
        # Run demo test
        print("🧪 Running demo tests...")
        result = subprocess.run(
            ["bash", "demo_test.sh", "http://localhost:8080"],
            cwd=SCRIPT_DIR
        )
        return result.returncode
    else:
        print(f"Unknown command: {command}")
        show_help()
        return 1

if __name__ == "__main__":
    sys.exit(main())
