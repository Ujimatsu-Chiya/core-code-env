"""Shared definitions/utilities for Java code generation."""

import os
import shutil
import subprocess
from dataclasses import dataclass
from typing import Dict, List, Tuple

from code_gen.utils import TypeEnum, TypeSpec, MethodDef, ClassDef
from code_gen.core.runtime_layout import get_runtime_path, get_rapidjson_helper_cpp

JAVA_TYPE_SPECS: Dict[TypeEnum, TypeSpec] = {
    TypeEnum.BOOL: TypeSpec("boolean", "false", "desBool", "serBool"),
    TypeEnum.INT: TypeSpec("int", "0", "desInt", "serInt"),
    TypeEnum.LONG: TypeSpec("long", "0L", "desLong", "serLong"),
    TypeEnum.DOUBLE: TypeSpec("double", "0.0", "desDouble", "serDouble"),
    TypeEnum.STRING: TypeSpec("String", '""', "desString", "serString"),
    TypeEnum.INT_LIST: TypeSpec("int[]", "new int[0]", "desIntList", "serIntList"),
    TypeEnum.INT_LIST_LIST: TypeSpec("int[][]", "new int[0][0]", "desIntListList", "serIntListList"),
    TypeEnum.DOUBLE_LIST: TypeSpec("double[]", "new double[0]", "desDoubleList", "serDoubleList"),
    TypeEnum.STRING_LIST: TypeSpec("String[]", "new String[0]", "desStringList", "serStringList"),
    TypeEnum.BOOL_LIST: TypeSpec("boolean[]", "new boolean[0]", "desBoolList", "serBoolList"),
    TypeEnum.TREENODE: TypeSpec("TreeNode", "null", "desTree", "serTree"),
    TypeEnum.LISTNODE: TypeSpec("ListNode", "null", "desLinkedList", "serLinkedList"),
    TypeEnum.LONG_LIST: TypeSpec("long[]", "new long[0]", "desLongList", "serLongList"),
    TypeEnum.NONE: TypeSpec("void", "/*none*/", "desNone", "serNone"),
}

TIME_COST_PATH = "time_cost.txt"
TMP_DIR = "tmp"
JAVA_RUNTIME_PATH = get_runtime_path("java")
JAVA_RUNTIME_FILES = [
    "JavaIoTools.java",
    "JavaNodeType.java",
    "JavaParseModule.h",
    "JavaParseModule.java",
    "JavaParseTools.java",
    "libjava_parse_module.so",
]


@dataclass
class JavaMethodDef(MethodDef):
    def generate(self) -> str:
        params_list: List[str] = []
        for p_type, p_name in zip(self.params_type, self.params_name):
            params_list.append(f"{JAVA_TYPE_SPECS[p_type].lang_type} {p_name}")
        ret_type = JAVA_TYPE_SPECS[self.return_type].lang_type
        return f"public {ret_type} {self.function_name}({', '.join(params_list)})"


@dataclass
class JavaClassDef(ClassDef):
    def __post_init__(self):
        self.constructor.function_name = self.name
        self.constructor.return_type = TypeEnum.NONE

    def constructor_generate(self):
        params_list: List[str] = []
        for p_type, p_name in zip(self.constructor.params_type, self.constructor.params_name):
            params_list.append(f"{JAVA_TYPE_SPECS[p_type].lang_type} {p_name}")
        return f"public {self.name}({', '.join(params_list)})"


def _build_java_runtime_lib(path: str = JAVA_RUNTIME_PATH) -> Tuple[int, str]:
    so_files = [filename for filename in os.listdir(path) if filename.startswith("libjava_") and filename.endswith(".so")]
    if so_files:
        return 0, ""

    java_home = os.environ.get("JAVA_HOME")
    if not java_home:
        return 1, "JAVA_HOME is not set. Run `script/setup_java.sh` or export JAVA_HOME first."

    result = subprocess.run(
        [
            "g++",
            "-fPIC",
            "-shared",
            "-o",
            "libjava_parse_module.so",
            "java_parse_module.cpp",
            get_rapidjson_helper_cpp(),
            f"-I{java_home}/include",
            f"-I{java_home}/include/linux",
        ],
        cwd=path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        return result.returncode, result.stderr
    return 0, ""


def _write_user_input(input_lines: List[str], tmp_dir: str = TMP_DIR) -> None:
    with open(os.path.join(tmp_dir, "user.in"), "w") as fp:
        for line in input_lines:
            fp.write(line + "\n")


def _write_main_java(solution_code: str, trailer_code: str, tmp_dir: str = TMP_DIR, path: str = JAVA_RUNTIME_PATH) -> None:
    with open(os.path.join(tmp_dir, "Main.java"), "w") as fp:
        with open(os.path.join(path, "java_header")) as fq:
            fp.write(fq.read() + "\n" + solution_code + trailer_code)


def _copy_runtime_files(path: str = JAVA_RUNTIME_PATH, tmp_dir: str = TMP_DIR) -> None:
    for filename in JAVA_RUNTIME_FILES:
        src = os.path.join(path, filename)
        dst = os.path.join(tmp_dir, filename)
        shutil.copy(src, dst)


def prepare_java_workspace(solution_code: str, trailer_code: str, input_lines: List[str], tmp_dir: str = TMP_DIR) -> Tuple[int, str]:
    os.makedirs(tmp_dir, exist_ok=True)
    _write_user_input(input_lines, tmp_dir)
    _write_main_java(solution_code, trailer_code, tmp_dir=tmp_dir)

    ret, message = _build_java_runtime_lib()
    if ret != 0:
        return ret, message

    _copy_runtime_files(tmp_dir=tmp_dir)
    return 0, ""


def compile_java_workspace(tmp_dir: str = TMP_DIR) -> Tuple[int, str]:
    java_files = sorted([filename for filename in os.listdir(tmp_dir) if filename.endswith(".java")])
    result = subprocess.run(
        ["javac", *java_files],
        cwd=tmp_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        return result.returncode, result.stderr
    return 0, ""


def run_java_workspace(tmp_dir: str = TMP_DIR) -> Tuple[int, str]:
    result = subprocess.run(
        ["java", "-Djava.library.path=.", "Main"],
        cwd=tmp_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        return result.returncode, result.stderr
    return 0, ""


def check_required_files(tmp_dir: str = TMP_DIR) -> Tuple[int, str]:
    required_files = ["user.out", "time_cost.txt"]
    files_in_directory = os.listdir(tmp_dir)
    missing_files = [file for file in required_files if file not in files_in_directory]
    if missing_files:
        return 1, f"Missing these files: {', '.join(missing_files)}"
    return 0, ""
