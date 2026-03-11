#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v apt >/dev/null 2>&1; then
  echo "[error] This script currently supports apt-based Linux only."
  exit 1
fi

echo "[info] Installing base build tools..."
sudo apt update
sudo apt install -y build-essential git curl

echo "[info] Setting up Python..."
bash "${script_dir}/setup_python.sh"

echo "[info] Setting up Java..."
bash "${script_dir}/setup_java.sh"

echo "[info] Setting up Go + goimports..."
bash "${script_dir}/setup_go.sh"
bash "${script_dir}/setup_goimports.sh"

echo "[info] Setting up Node.js + TypeScript..."
bash "${script_dir}/setup_node_ts.sh"

echo "[done] Development environment setup finished."
