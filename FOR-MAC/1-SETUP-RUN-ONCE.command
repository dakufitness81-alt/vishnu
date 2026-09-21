#!/bin/bash
cd "$(dirname "$0")/.."
echo
echo "============================================"
echo "  SETUP - first time only (1 to 3 minutes)"
echo "============================================"
echo
if ! command -v python3 >/dev/null 2>&1; then
  echo
  echo  Python3 was NOT found. Do this once:
  echo
  echo   1. Open Terminal (search "Terminal" in Spotlight)
  echo   2. Type:  xcode-select --install   and press Enter,
  echo      then click "Install" in the popup
  echo   3. When finished, double-click THIS file again
  echo
  read -n 1
  exit 1
fi
echo "  Python found. Downloading free tools (please wait)..."
python3 -m venv .venv
./.venv/bin/pip install --quiet --upgrade pip
./.venv/bin/pip install --quiet -r requirements.txt
if [ $? -ne 0 ]; then
  echo
  echo  Something failed. Check your internet and double-click me again.
  echo
  read -n 1
  exit 1
fi
echo
echo "============================================"
echo "  DONE! Setup finished."
echo
echo "  Next step:"
echo "  1. Open config.yaml, put your handle"
echo "  2. Double-click 2-MAKE-VIDEO.command"
echo "============================================"
echo
read -n 1
