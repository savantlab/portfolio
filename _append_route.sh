#!/bin/bash
set -euo pipefail
cd /flask
cp app.py app.py.bak_$(date +%Y%m%d%H%M%S)
if ! grep -q "def gorgon_resume_html" app.py; then
  cat _route_snippet.txt >> app.py
fi
pkill -HUP -f "gunicorn.*app:app" || true
sleep 1
