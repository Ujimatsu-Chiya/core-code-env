#!/usr/bin/env bash
set -euo pipefail

if ! command -v apt >/dev/null 2>&1; then
  echo "[error] This script currently supports apt-based Linux only."
  exit 1
fi

echo "[info] Installing C/C++ build dependencies..."
sudo apt update
sudo apt install -y build-essential pkg-config libglib2.0-dev uthash-dev

echo "[info] C/C++ installation check"
gcc --version | head -n 1
g++ --version | head -n 1
pkg-config --modversion glib-2.0

if [ ! -f /usr/include/uthash.h ]; then
  echo "[error] uthash.h was not found after installing uthash-dev."
  exit 1
fi

echo "[done] C/C++ environment is ready."
