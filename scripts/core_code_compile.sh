#!/usr/bin/env bash
set -euo pipefail

runtime_root="${CORE_CODE_RUNTIME_ROOT:-${CODE_GEN_RUNTIME_ROOT:-/share/core-code-env/runtimes}}"
include_root="${CORE_CODE_INCLUDE_ROOT:-/include/core-code-env}"
lib_dir="${CORE_CODE_LIB_DIR:-/lib}"

die() {
  echo "core-code compile error: $*" >&2
  exit 1
}

require_file() {
  [ -f "$1" ] || die "missing file: $1"
}

patch_cpp_user_input_guard() {
  local inserted=0
  local line
  : > main.cc.tmp
  while IFS= read -r line || [ -n "$line" ]; do
    printf '%s\n' "$line" >> main.cc.tmp
    if [ "$inserted" -eq 0 ] && [[ "$line" == *"int main() {"* ]]; then
      printf '%s\n' '    std::ofstream __core_code_user_in_guard("user.in", std::ios::app);' >> main.cc.tmp
      printf '%s\n' '    __core_code_user_in_guard.close();' >> main.cc.tmp
      inserted=1
    fi
  done < main.cc
  [ "$inserted" -eq 1 ] || die "cannot locate int main() in generated C++ source"
  mv main.cc.tmp main.cc
}

patch_c_user_input_guard() {
  local inserted=0
  local line
  : > main.c.tmp
  while IFS= read -r line || [ -n "$line" ]; do
    printf '%s\n' "$line" >> main.c.tmp
    if [ "$inserted" -eq 0 ] && [[ "$line" == *"int main() {"* ]]; then
      printf '%s\n' '    FILE* __core_code_user_in_guard = fopen("user.in", "a");' >> main.c.tmp
      printf '%s\n' '    if (__core_code_user_in_guard) fclose(__core_code_user_in_guard);' >> main.c.tmp
      inserted=1
    fi
  done < main.c
  [ "$inserted" -eq 1 ] || die "cannot locate int main() in generated C source"
  mv main.c.tmp main.c
}

cpp_std_flag() {
  case "${HYDRO_LANG:-}" in
    cc.cc98*|core.cc98*) echo "-std=c++98" ;;
    cc.cc11*|core.cc11*) echo "-std=c++11" ;;
    cc.cc14*|core.cc14*) echo "-std=c++14" ;;
    cc.cc17*|core.cc17*) echo "-std=c++17" ;;
    cc.cc20*|core.cc20*) echo "-std=c++20" ;;
    *) echo "-std=c++17" ;;
  esac
}

opt_flag() {
  case "${HYDRO_LANG:-}" in
    *o2) echo "-O2" ;;
    *) echo "" ;;
  esac
}

compile_cpp() {
  require_file "$runtime_root/cpp/cpp_header"
  require_file "foo.cc"
  require_file "main_trailer.cpp"

  cat "$runtime_root/cpp/cpp_header" foo.cc main_trailer.cpp > main.cc
  patch_cpp_user_input_guard
  g++ -x c++ main.cc -o foo \
    -lm -fno-stack-limit -fdiagnostics-color=always \
    "$(cpp_std_flag)" $(opt_flag) \
    -I/include -I"$include_root" -I"$include_root/cpp" -I"$runtime_root/cpp" \
    -L"$lib_dir" -lcpp_parse_tools -Wl,-rpath,"$lib_dir"
}

compile_c() {
  require_file "$runtime_root/c/c_header"
  require_file "$runtime_root/c/c_io_tools.c"
  require_file "foo.c"
  require_file "main_trailer.c"
  command -v pkg-config >/dev/null 2>&1 || die "pkg-config is required for C submissions"
  # The HydroOJ rootfs exposes development metadata under $lib_dir/pkgconfig,
  # while Nix's pkg-config keeps its original /nix/store default search path.
  # Restrict lookup to the metadata intentionally exposed by the sandbox and
  # do not depend on environment inherited by an individual judge worker.
  unset PKG_CONFIG_PATH
  export PKG_CONFIG_LIBDIR="$lib_dir/pkgconfig"

  pkg-config --exists glib-2.0 || die "glib-2.0 development files are required for C submissions"

  cat "$runtime_root/c/c_header" foo.c main_trailer.c > main.c
  patch_c_user_input_guard
  glib_cflags="$(pkg-config --cflags glib-2.0)"
  glib_libs="$(pkg-config --libs glib-2.0)"
  gcc -x c main.c "$runtime_root/c/c_io_tools.c" -o foo \
    -lm -fno-stack-limit -fdiagnostics-color=always \
    $glib_cflags -I/include -I"$include_root" -I"$include_root/c" -I"$runtime_root/c" \
    -L"$lib_dir" -lc_parse_tools -Wl,-rpath,"$lib_dir" $glib_libs
}

compile_python() {
  require_file "$runtime_root/py/py_header"
  require_file "foo.py"
  require_file "main_trailer.py"

  {
    printf 'import sys\n'
    printf 'sys.path.insert(0, "%s")\n' "$runtime_root/py"
    cat "$runtime_root/py/py_header" foo.py main_trailer.py
  } > main.py
  mv main.py foo.py
  python3 -c "import py_compile; py_compile.compile('foo.py', doraise=True)"
  mv foo.py foo
}

compile_java() {
  require_file "$runtime_root/java/java_header"
  require_file "Main.java"
  require_file "main_trailer.java"

  mv Main.java Solution.java
  cat "$runtime_root/java/java_header" Solution.java main_trailer.java > Main.java
  mkdir -p .core_code_java_classes
  javac -d .core_code_java_classes -encoding utf8 Main.java "$runtime_root"/java/Java*.java
  jar cvf Main.jar -C .core_code_java_classes . >/dev/null
}

compile_js() {
  require_file "$runtime_root/js/js_header"
  require_file "$runtime_root/js/js_io_tools.js"
  require_file "$runtime_root/js/js_parse_tools.js"
  require_file "$runtime_root/js/js_type_node.js"
  require_file "foo.js"
  require_file "main_trailer.js"

  {
    printf '%s\n' '"use strict";'
    printf 'const JsIoTools = require("%s/js/js_io_tools");\n' "$runtime_root"
    printf 'const JsParseTools = require("%s/js/js_parse_tools");\n' "$runtime_root"
    printf 'const JsTypeNode = require("%s/js/js_type_node");\n' "$runtime_root"
    printf '%s\n' 'const fs = require("fs");'
    printf '%s\n' '// The user'\''s code will be inserted below here.'
  } > .core_code_js_header.js
  cat .core_code_js_header.js foo.js main_trailer.js > .core_code_js_main.js
  mv .core_code_js_main.js foo.js
  node --check foo.js
}

compile_ts() {
  require_file "$runtime_root/ts/ts_header"
  require_file "$runtime_root/ts/ts_io_tools.ts"
  require_file "$runtime_root/ts/ts_parse_tools.ts"
  require_file "$runtime_root/ts/ts_type_node.ts"
  require_file "foo.ts"
  require_file "main_trailer.ts"

  {
    printf '%s\n' 'declare const require: any;'
    printf '%s\n' 'declare const process: any;'
    printf 'const JsTypeNode = require("%s/js/js_type_node");\n' "$runtime_root"
    printf '%s\n' 'type TreeNode = any;'
    printf '%s\n' 'type ListNode = any;'
    printf '%s\n' 'const TreeNode = JsTypeNode.TreeNode;'
    printf '%s\n' 'const ListNode = JsTypeNode.ListNode;'
    printf 'const JsIoTools = require("%s/js/js_io_tools");\n' "$runtime_root"
    printf '%s\n' 'type StdinWrapper = any;'
    printf '%s\n' 'type StdoutWrapper = any;'
    printf '%s\n' 'const StdinWrapper = JsIoTools.StdinWrapper;'
    printf '%s\n' 'const StdoutWrapper = JsIoTools.StdoutWrapper;'
    printf 'const TsParseTools = require("%s/js/js_parse_tools");\n' "$runtime_root"
    printf '%s\n' 'const fs = require("fs");'
    printf '%s\n' '// The user'\''s code will be inserted below here.'
  } > .core_code_ts_header.ts
  cat .core_code_ts_header.ts foo.ts main_trailer.ts > main.ts
  tsc --target es2020 --module commonjs main.ts
  mv main.js foo.js
  node --check foo.js
}

compile_go() {
  require_file "$runtime_root/go/go_header"
  require_file "$runtime_root/go/go_io_tools.go"
  require_file "$runtime_root/go/go_parse_tools.go"
  require_file "$runtime_root/go/go_type_node.go"
  require_file "foo.go"
  require_file "main_trailer.go"

  cat "$runtime_root/go/go_header" foo.go main_trailer.go > main.go
  cp "$runtime_root/go/go_io_tools.go" .
  cp "$runtime_root/go/go_parse_tools.go" .
  cp "$runtime_root/go/go_type_node.go" .
  chmod u+w go_io_tools.go go_parse_tools.go go_type_node.go
  export GOCACHE="${GOCACHE:-/tmp/go-build-cache}"
  mkdir -p "$GOCACHE"
  if command -v goimports >/dev/null 2>&1; then
    goimports -w main.go
  else
    die "goimports is required for Go core-code submissions"
  fi
  gofmt -w go_io_tools.go go_parse_tools.go go_type_node.go
  go build -o foo main.go go_io_tools.go go_parse_tools.go go_type_node.go
}

case "${HYDRO_LANG:-}" in
  c|core.c)
    compile_c
    ;;
  cc|cc.*|core.cc*)
    compile_cpp
    ;;
  py|py.py3|core.py|core.py3)
    compile_python
    ;;
  java|core.java)
    compile_java
    ;;
  js|js.*|core.js|core.js.*)
    compile_js
    ;;
  ts|ts.*|core.ts|core.ts.*)
    compile_ts
    ;;
  go|core.go)
    compile_go
    ;;
  *)
    die "unsupported HYDRO_LANG: ${HYDRO_LANG:-<empty>}"
    ;;
esac
