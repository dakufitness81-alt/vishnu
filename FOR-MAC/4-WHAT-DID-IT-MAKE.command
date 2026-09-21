#!/bin/bash
cd "$(dirname "$0")/.."
echo
if [ ! -x .venv/bin/python ]; then
  echo "  First time here? Double-click 1-SETUP-RUN-ONCE.command first."
  echo
  read -n 1
  exit 1
fi
./.venv/bin/python -m agent status
echo
read -n 1
