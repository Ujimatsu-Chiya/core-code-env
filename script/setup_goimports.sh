#!/usr/bin/env bash
set -euo pipefail

if ! command -v go >/dev/null 2>&1; then
  echo "[error] go is not installed. Install Go first, e.g.:"
  echo "        sudo apt update && sudo apt install -y golang-go"
  exit 1
fi

echo "[info] Installing goimports..."
if go install golang.org/x/tools/cmd/goimports@latest; then
  :
else
  echo "[warn] Default GOPROXY failed, retry with goproxy.cn..."
  go env -w GOPROXY=https://goproxy.cn,direct
  go install golang.org/x/tools/cmd/goimports@latest
fi

go_bin="$(go env GOBIN)"
if [ -z "${go_bin}" ]; then
  go_bin="$(go env GOPATH)/bin"
fi
goimports_path="${go_bin}/goimports"

if [ ! -x "${goimports_path}" ]; then
  echo "[error] goimports was not found at ${goimports_path}"
  exit 1
fi

if [[ ":${PATH}:" != *":${go_bin}:"* ]]; then
  echo "[info] Adding ${go_bin} to ~/.bashrc"
  if ! grep -q "export PATH=.*${go_bin}" ~/.bashrc; then
    echo "export PATH=\$PATH:${go_bin}" >> ~/.bashrc
  fi
fi

echo "[info] goimports path: ${goimports_path}"
echo "[done] goimports is ready."
