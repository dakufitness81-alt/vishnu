#!/bin/bash
cd "$(dirname "$0")/.."
echo
echo "============================================"
echo "  MAKING TODAY'S VIDEO (30 to 90 seconds)"
echo "============================================"
echo
if [ ! -x .venv/bin/python ]; then
  echo "  First time here? Double-click 1-SETUP-RUN-ONCE.command first."
  echo
  read -n 1
  exit 1
fi
./.venv/bin/python -m agent run
echo
echo "  Your video is ready here:"
echo "  vishnu folder > output > posts > newest folder > video.mp4"
echo
read -n 1
