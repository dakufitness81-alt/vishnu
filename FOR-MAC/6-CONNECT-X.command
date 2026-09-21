#!/bin/bash
cd "$(dirname "$0")/.."
echo
echo "============================================"
echo "  CONNECT YOUR X (TWITTER) ACCOUNT"
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
./.venv/bin/python -m agent auth x
echo
read -n 1
