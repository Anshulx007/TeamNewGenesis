#!/bin/bash
# SahajAI Quick Deploy Wrapper
# Usage: ./deploy.sh

cd "$(dirname "$0")" || exit 1
python3 full_deploy.py "$@"
