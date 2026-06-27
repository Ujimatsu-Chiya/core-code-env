#!/usr/bin/env bash
set -euo pipefail

PREFIX="${1:-/usr/local}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

CXX="${CXX:-g++}"
RAPIDJSON_CFLAGS="${RAPIDJSON_CFLAGS:-}"

copy_optional_headers() {
  local source_dir="$1"
  local target_dir="$2"
  local -a headers=("${source_dir}"/*.h)

  if [ -e "${headers[0]}" ]; then
    cp "${headers[@]}" "${target_dir}/"
  fi
}

if ! command -v "$CXX" >/dev/null 2>&1; then
  echo "C++ compiler not found: $CXX" >&2
  echo "Set CXX=/path/to/g++ or install g++ before running this script." >&2
  exit 1
fi

mkdir -p \
  "$PREFIX/share/core-code-env" \
  "$PREFIX/share/core-code-env/runtimes" \
  "$PREFIX/include/core-code-env" \
  "$PREFIX/lib"

cp -a "$REPO_ROOT/runtimes/." "$PREFIX/share/core-code-env/runtimes/"
cp "$REPO_ROOT/rapidjson_helper.cpp" "$PREFIX/share/core-code-env/rapidjson_helper.cpp"
cp "$REPO_ROOT/rapidjson_helper.h" "$PREFIX/share/core-code-env/rapidjson_helper.h"

mkdir -p \
  "$PREFIX/include/core-code-env/c" \
  "$PREFIX/include/core-code-env/cpp" \
  "$PREFIX/include/core-code-env/java" \
  "$PREFIX/include/core-code-env/py"

cp "$REPO_ROOT/runtimes/c/"*.h "$PREFIX/include/core-code-env/c/"
cp "$REPO_ROOT/runtimes/cpp/"*.h "$PREFIX/include/core-code-env/cpp/"
copy_optional_headers "$REPO_ROOT/runtimes/java" "$PREFIX/include/core-code-env/java"
copy_optional_headers "$REPO_ROOT/runtimes/py" "$PREFIX/include/core-code-env/py"
cp "$REPO_ROOT/rapidjson_helper.h" "$PREFIX/include/core-code-env/rapidjson_helper.h"

"$CXX" -shared -fPIC \
  -o "$PREFIX/lib/libc_parse_tools.so" \
  "$REPO_ROOT/runtimes/c/c_parse_tools.c" \
  "$REPO_ROOT/runtimes/c/c_parse_module.cpp" \
  "$REPO_ROOT/rapidjson_helper.cpp" \
  -I"$REPO_ROOT" -I"$REPO_ROOT/runtimes/c" $RAPIDJSON_CFLAGS

"$CXX" -shared -fPIC \
  -o "$PREFIX/lib/libcpp_parse_tools.so" \
  "$REPO_ROOT/runtimes/cpp/cpp_parse_tools.cpp" \
  "$REPO_ROOT/runtimes/cpp/cpp_parse_module.cpp" \
  "$REPO_ROOT/rapidjson_helper.cpp" \
  -I"$REPO_ROOT" -I"$REPO_ROOT/runtimes/cpp" $RAPIDJSON_CFLAGS

cp "$PREFIX/lib/libc_parse_tools.so" "$PREFIX/share/core-code-env/runtimes/c/libc_parse_tools.so"
cp "$PREFIX/lib/libcpp_parse_tools.so" "$PREFIX/share/core-code-env/runtimes/cpp/libcpp_parse_tools.so"

cat > "$PREFIX/share/core-code-env/env.sh" <<EOF
export CODE_GEN_CORE_ROOT="$PREFIX/share/core-code-env"
export CODE_GEN_RUNTIME_ROOT="$PREFIX/share/core-code-env/runtimes"
export CODE_GEN_RAPIDJSON_HELPER_CPP="$PREFIX/share/core-code-env/rapidjson_helper.cpp"
export CODE_GEN_RAPIDJSON_HELPER_INCLUDE_DIR="$PREFIX/share/core-code-env"
EOF

printf 'Installed core-code-env runtime to %s\n' "$PREFIX"
printf 'Runtime root: %s\n' "$PREFIX/share/core-code-env/runtimes"
printf 'C lib: %s\n' "$PREFIX/lib/libc_parse_tools.so"
printf 'C++ lib: %s\n' "$PREFIX/lib/libcpp_parse_tools.so"
