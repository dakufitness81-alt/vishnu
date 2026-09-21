#!/usr/bin/env bash
# One-time setup for Mac / Linux — run from inside the vishnu folder:
#   bash setup.sh
set -e
cd "$(dirname "$0")"

echo "→ Setting up Python environment..."
python3 -m venv .venv

echo "→ Installing packages (this takes 1-2 minutes)..."
./.venv/bin/pip install --quiet --upgrade pip
./.venv/bin/pip install --quiet -r requirements.txt

echo ""
echo "✅ Done! Next steps:"
echo "   1) Edit config.yaml  →  set your handle"
echo "   2) ./.venv/bin/python -m agent init"
echo "   3) ./.venv/bin/python -m agent run --dry-run"
