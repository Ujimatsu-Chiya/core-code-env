{ pkgs ? import <nixpkgs> {}, src ? ../. }:

let
  pythonForBuild = pkgs.python3.withPackages (ps: [ ps.setuptools ]);
in
pkgs.stdenv.mkDerivation {
  pname = "core-code-env-runtime";
  version = "0.1.0";
  inherit src;

  # Build only the core-code-env runtime artifacts here. The HydroOJ rootfs
  # decides which compilers, headers, and pkg-config files are exposed inside
  # the sandbox; keep those as passthru metadata so this output layout does not
  # change when the sandbox is already working.
  nativeBuildInputs = [
    pkgs.gcc
    pythonForBuild
    pkgs.openjdk_headless
  ];

  passthru.sandboxRuntimeInputs = with pkgs; [
    pkg-config
    glib
    glib.dev
    uthash
  ];

  buildPhase = ''
    runHook preBuild

    g++ -shared -fPIC \
      -o libc_parse_tools.so \
      runtimes/c/c_io_tools.c \
      runtimes/c/c_parse_tools.c \
      runtimes/c/c_parse_module.cpp \
      rapidjson_helper.cpp \
      -I. -Iruntimes/c -isystem ${pkgs.rapidjson}/include

    g++ -shared -fPIC \
      -o libcpp_parse_tools.so \
      runtimes/cpp/cpp_parse_tools.cpp \
      runtimes/cpp/cpp_parse_module.cpp \
      rapidjson_helper.cpp \
      -I. -Iruntimes/cpp -isystem ${pkgs.rapidjson}/include

    (
      cd runtimes/py
      CODE_GEN_RAPIDJSON_HELPER_CPP="$PWD/../../rapidjson_helper.cpp" \
      CODE_GEN_RAPIDJSON_HELPER_INCLUDE_DIR="$PWD/../.." \
      CPLUS_INCLUDE_PATH="${pkgs.rapidjson}/include''${CPLUS_INCLUDE_PATH:+:$CPLUS_INCLUDE_PATH}" \
      python3 setup.py build --build-lib .
    )

    g++ -shared -fPIC \
      -o libjava_parse_module.so \
      runtimes/java/java_parse_module.cpp \
      rapidjson_helper.cpp \
      -I. -Iruntimes/java \
      -I${pkgs.openjdk_headless}/include \
      -I${pkgs.openjdk_headless}/include/linux \
      -isystem ${pkgs.rapidjson}/include

    runHook postBuild
  '';

  installPhase = ''
    runHook preInstall

    mkdir -p \
      $out/share/core-code-env/runtimes \
      $out/include/core-code-env/c \
      $out/include/core-code-env/cpp \
      $out/lib

    cp -r runtimes/. $out/share/core-code-env/runtimes/
    cp rapidjson_helper.cpp rapidjson_helper.h $out/share/core-code-env/
    cp scripts/core_code_compile.sh $out/share/core-code-env/core_code_compile.sh
    chmod +x $out/share/core-code-env/core_code_compile.sh

    cp runtimes/c/*.h $out/include/core-code-env/c/
    cp runtimes/cpp/*.h $out/include/core-code-env/cpp/
    cp rapidjson_helper.h $out/include/core-code-env/rapidjson_helper.h

    cp libc_parse_tools.so $out/lib/
    cp libcpp_parse_tools.so $out/lib/
    cp libjava_parse_module.so $out/lib/
    cp libc_parse_tools.so $out/share/core-code-env/runtimes/c/
    cp libcpp_parse_tools.so $out/share/core-code-env/runtimes/cpp/
    cp libjava_parse_module.so $out/share/core-code-env/runtimes/java/

    cat > $out/share/core-code-env/env.sh <<EOF
export CODE_GEN_CORE_ROOT=$out/share/core-code-env
export CODE_GEN_RUNTIME_ROOT=$out/share/core-code-env/runtimes
export CODE_GEN_RAPIDJSON_HELPER_CPP=$out/share/core-code-env/rapidjson_helper.cpp
export CODE_GEN_RAPIDJSON_HELPER_INCLUDE_DIR=$out/share/core-code-env
EOF

    runHook postInstall
  '';
}
