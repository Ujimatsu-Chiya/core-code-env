"""Shared definitions/utilities for TypeScript code generation."""

import os
import shutil
import subprocess
from dataclasses import dataclass
from typing import Dict, List, Tuple

from utils import TypeEnum, TypeSpec, MethodDef, ClassDef

TS_TYPE_SPECS: Dict[TypeEnum, TypeSpec] = {
    TypeEnum.BOOL: TypeSpec("boolean", "false", "desBool", "serBool"),
    TypeEnum.INT: TypeSpec("number", "0", "desNumber", "serNumber"),
    TypeEnum.LONG: TypeSpec("number", "0", "desNumber", "serNumber"),
    TypeEnum.DOUBLE: TypeSpec("number", "0.0", "desNumber", "serNumber"),
    TypeEnum.STRING: TypeSpec("string", '""', "desString", "serString"),
    TypeEnum.INT_LIST: TypeSpec("number[]", "[]", "desNumberList", "serNumberList"),
    TypeEnum.INT_LIST_LIST: TypeSpec("number[][]", "[]", "desNumberListList", "serNumberListList"),
    TypeEnum.DOUBLE_LIST: TypeSpec("number[]", "[]", "desNumberList", "serNumberList"),
    TypeEnum.STRING_LIST: TypeSpec("string[]", "[]", "desStringList", "serStringList"),
    TypeEnum.BOOL_LIST: TypeSpec("boolean[]", "[]", "desBoolList", "serBoolList"),
    TypeEnum.TREENODE: TypeSpec("TreeNode | null", "null", "desTree", "serTree"),
    TypeEnum.LISTNODE: TypeSpec("ListNode | null", "null", "desLinkedList", "serLinkedList"),
    TypeEnum.LONG_LIST: TypeSpec("number[]", "[]", "desNumberList", "serNumberList"),
    TypeEnum.NONE: TypeSpec("void", "undefined", "desNone", "serNone"),
}

TIME_COST_PATH = "time_cost.txt"
TMP_DIR = "tmp"
TS_RUNTIME_PATH = "typescript"
TS_RUNTIME_FILES = [
    "ts_io_tools.ts",
    "ts_parse_tools.ts",
    "ts_type_node.ts",
]


@dataclass
class TsMethodDef(MethodDef):
    def generate(self) -> str:
        params_list: List[str] = []
        for p_type, p_name in zip(self.params_type, self.params_name):
            params_list.append(f"{p_name}: {TS_TYPE_SPECS[p_type].lang_type}")
        ret_type = TS_TYPE_SPECS[self.return_type].lang_type
        return f"{self.function_name}({', '.join(params_list)}): {ret_type}"


@dataclass
class TsClassDef(ClassDef):
    def __post_init__(self):
        self.constructor.function_name = "constructor"
        self.constructor.return_type = TypeEnum.NONE

    def constructor_generate(self):
        params_list: List[str] = []
        for p_type, p_name in zip(self.constructor.params_type, self.constructor.params_name):
            params_list.append(f"{p_name}: {TS_TYPE_SPECS[p_type].lang_type}")
        return f"constructor({', '.join(params_list)})"


def _write_user_input(input_lines: List[str], tmp_dir: str = TMP_DIR) -> None:
    with open(os.path.join(tmp_dir, "user.in"), "w") as fp:
        for line in input_lines:
            fp.write(line + "\n")


def _write_main_ts(solution_code: str, trailer_code: str, tmp_dir: str = TMP_DIR, path: str = TS_RUNTIME_PATH) -> None:
    with open(os.path.join(tmp_dir, "main.ts"), "w") as fp:
        with open(os.path.join(path, "ts_header")) as fq:
            fp.write(fq.read() + "\n" + solution_code + trailer_code)


def _copy_runtime_files(path: str = TS_RUNTIME_PATH, tmp_dir: str = TMP_DIR) -> None:
    for filename in TS_RUNTIME_FILES:
        src = os.path.join(path, filename)
        dst = os.path.join(tmp_dir, filename)
        shutil.copy(src, dst)


def prepare_ts_workspace(solution_code: str, trailer_code: str, input_lines: List[str], tmp_dir: str = TMP_DIR) -> Tuple[int, str]:
    os.makedirs(tmp_dir, exist_ok=True)
    _write_user_input(input_lines, tmp_dir)
    _write_main_ts(solution_code, trailer_code, tmp_dir=tmp_dir)
    _copy_runtime_files(tmp_dir=tmp_dir)
    return 0, ""


def compile_ts_workspace(tmp_dir: str = TMP_DIR) -> Tuple[int, str]:
    try:
        result = subprocess.run(
            ["tsc", "--target", "es6", "--module", "commonjs", "main.ts"],
            cwd=tmp_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except FileNotFoundError:
        return 1, "tsc is not found in PATH."
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip()
        return result.returncode, message
    return 0, ""


def run_ts_workspace(tmp_dir: str = TMP_DIR) -> Tuple[int, str]:
    try:
        result = subprocess.run(
            ["node", "main.js"],
            cwd=tmp_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except FileNotFoundError:
        return 1, "node is not found in PATH."
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip()
        return result.returncode, message
    return 0, ""


def check_required_files(tmp_dir: str = TMP_DIR) -> Tuple[int, str]:
    required_files = ["user.out", "time_cost.txt"]
    files_in_directory = os.listdir(tmp_dir)
    missing_files = [file for file in required_files if file not in files_in_directory]
    if missing_files:
        return 1, f"Missing these files: {', '.join(missing_files)}"
    return 0, ""
