#!/bin/bash
cd "$(dirname "$0")/.."
echo
echo "============================================"
echo "  VIDEO FROM YOUR OWN IDEA"
echo "============================================"
echo
if [ ! -x .venv/bin/python ]; then
  echo "  First time here? Double-click 1-SETUP-RUN-ONCE.command first."
  echo
  read -n 1
  exit 1
fi
printf "Type your video idea in English, then press Enter: "
read IDEA
if [ -z "$IDEA" ]; then
  echo "  You need to type an idea. Try again."
  read -n 1
  exit 1
fi
./.venv/bin/python -m agent run --idea "$IDEA"
echo
read -n 1
