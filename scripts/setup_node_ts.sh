#!/usr/bin/env bash
set -euo pipefail

if ! command -v apt >/dev/null 2>&1; then
  echo "[error] This script currently supports apt-based Linux only."
  exit 1
fi

echo "[info] Installing Node.js and npm..."
sudo apt update
sudo apt install -y nodejs npm

echo "[info] Installing TypeScript compiler (tsc)..."
if command -v tsc >/dev/null 2>&1; then
  echo "[info] tsc already exists: $(command -v tsc)"
else
  sudo npm install -g typescript
fi

echo "[info] Installing Node.js TypeScript definitions..."
if npm root -g >/dev/null 2>&1 && [ -d "$(npm root -g)/@types/node" ]; then
  echo "[info] @types/node already exists: $(npm root -g)/@types/node"
else
  sudo npm install -g @types/node
fi

echo "[info] Node/TypeScript installation check"
node --version
npm --version
tsc --version

echo "[done] Node.js + TypeScript environment is ready."
