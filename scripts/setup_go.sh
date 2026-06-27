#!/usr/bin/env bash
set -euo pipefail

if ! command -v apt >/dev/null 2>&1; then
  echo "[error] This script currently supports apt-based Linux only."
  exit 1
fi

bashrc="${HOME}/.bashrc"

ensure_bashrc_line() {
  local line="$1"
  if [ -f "${bashrc}" ] && grep -Fxq "${line}" "${bashrc}"; then
    return
  fi
  echo "${line}" >> "${bashrc}"
}

add_path_if_exists() {
  local dir="$1"
  if [ -d "${dir}" ] && [[ ":${PATH}:" != *":${dir}:"* ]]; then
    export PATH="${dir}:${PATH}"
  fi
}

add_path_if_exists "/usr/local/go/bin"
add_path_if_exists "${HOME}/go/bin"

if ! command -v go >/dev/null 2>&1; then
  if [ -x "/usr/local/go/bin/go" ]; then
    export PATH="/usr/local/go/bin:${PATH}"
  else
    echo "[info] go was not found in PATH. Installing Go via apt..."
    sudo apt update
    sudo apt install -y golang-go
  fi
fi

if ! command -v go >/dev/null 2>&1; then
  echo "[error] go is still not available after setup."
  echo "        Check whether golang-go installed successfully, or add Go's bin directory to PATH."
  exit 1
fi

if [ -z "${GOPATH:-}" ]; then
  GOPATH="$(go env GOPATH)"
  if [ -z "${GOPATH}" ]; then
    GOPATH="${HOME}/go"
  fi
  export GOPATH
  echo "[info] GOPATH was not set; using ${GOPATH}"
else
  echo "[info] GOPATH is already set to ${GOPATH}"
fi

mkdir -p "${GOPATH}/bin"

if [[ ":${PATH}:" != *":${GOPATH}/bin:"* ]]; then
  export PATH="${PATH}:${GOPATH}/bin"
fi

ensure_bashrc_line "export GOPATH=${GOPATH}"
ensure_bashrc_line "export PATH=\$PATH:/usr/local/go/bin:${GOPATH}/bin"

echo "[info] go path: $(command -v go)"
echo "[info] GOPATH: ${GOPATH}"
go version
echo "[done] Go environment is ready."
