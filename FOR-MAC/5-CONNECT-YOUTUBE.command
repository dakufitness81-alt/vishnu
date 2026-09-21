#!/bin/bash
cd "$(dirname "$0")/.."
echo
echo "============================================"
echo "  CONNECT YOUR YOUTUBE CHANNEL"
echo "============================================"
echo
echo "  This will open a link. Approve it, then paste"
echo "  the code you see here."
echo
if [ ! -x .venv/bin/python ]; then
  echo "  First time here? Double-click 1-SETUP-RUN-ONCE.command first."
  echo
  read -n 1
  exit 1
fi
./.venv/bin/pip install --quiet google-api-python-client google-auth-httplib2 google-auth-oauthlib
./.venv/bin/python -m agent auth youtube
echo
read -n 1
