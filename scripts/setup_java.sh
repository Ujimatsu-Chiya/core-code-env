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

detect_java_home() {
  local java_bin
  java_bin="$(command -v javac || command -v java || true)"
  if [ -z "${java_bin}" ]; then
    return 1
  fi
  dirname "$(dirname "$(readlink -f "${java_bin}")")"
}

if ! command -v java >/dev/null 2>&1 || ! command -v javac >/dev/null 2>&1; then
  echo "[info] Installing OpenJDK 21..."
  sudo apt update
  sudo apt install -y openjdk-21-jdk
fi

if ! command -v java >/dev/null 2>&1 || ! command -v javac >/dev/null 2>&1; then
  echo "[error] Java/JDK is still not available after setup."
  exit 1
fi

if [ -z "${JAVA_HOME:-}" ]; then
  JAVA_HOME="$(detect_java_home)"
  export JAVA_HOME
  echo "[info] JAVA_HOME was not set; using ${JAVA_HOME}"
else
  echo "[info] JAVA_HOME is already set to ${JAVA_HOME}"
fi

if [ ! -x "${JAVA_HOME}/bin/java" ] || [ ! -x "${JAVA_HOME}/bin/javac" ]; then
  echo "[error] JAVA_HOME does not point to a JDK: ${JAVA_HOME}"
  exit 1
fi

if [[ ":${PATH}:" != *":${JAVA_HOME}/bin:"* ]]; then
  export PATH="${JAVA_HOME}/bin:${PATH}"
fi

ensure_bashrc_line "export JAVA_HOME=${JAVA_HOME}"
ensure_bashrc_line "export PATH=\$JAVA_HOME/bin:\$PATH"

echo "[info] JAVA_HOME: ${JAVA_HOME}"
java -version
javac -version
echo "[done] Java environment is ready."
