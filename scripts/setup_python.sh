#!/usr/bin/env bash
set -euo pipefail

if ! command -v apt >/dev/null 2>&1; then
  echo "[error] This script currently supports apt-based Linux only."
  exit 1
fi

echo "[info] Installing Python dependencies..."
sudo apt update
sudo apt install -y python3 python3-dev python3-pip python3-venv

echo "[info] Python installation check"
python3 --version
python3 -c "import sys; print(sys.executable)"

if command -v python3-config >/dev/null 2>&1; then
  echo "[info] python3-config includes:"
  python3-config --includes
fi

echo "[done] Python environment is ready."
