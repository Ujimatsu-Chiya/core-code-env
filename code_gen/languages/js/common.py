"""Shared definitions/utilities for JavaScript code generation."""

import os
import shutil
import subprocess
from dataclasses import dataclass
from typing import Dict, List, Tuple

from code_gen.utils import TypeEnum, TypeSpec, MethodDef, ClassDef
from code_gen.core.runtime_layout import get_runtime_path

JS_TYPE_SPECS: Dict[TypeEnum, TypeSpec] = {
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
JS_RUNTIME_PATH = get_runtime_path("js")
JS_RUNTIME_FILES = [
    "js_io_tools.js",
    "js_parse_tools.js",
    "js_type_node.js",
]


@dataclass
class JsMethodDef(MethodDef):
    def generate(self) -> str:
        return f"{self.function_name}({', '.join(self.params_name)})"


@dataclass
class JsClassDef(ClassDef):
    def __post_init__(self):
        self.constructor.function_name = "constructor"
        self.constructor.return_type = TypeEnum.NONE

    def constructor_generate(self):
        return f"constructor({', '.join(self.constructor.params_name)})"


def _write_user_input(input_lines: List[str], tmp_dir: str = TMP_DIR) -> None:
    with open(os.path.join(tmp_dir, "user.in"), "w") as fp:
        for line in input_lines:
            fp.write(line + "\n")


def _write_main_js(solution_code: str, trailer_code: str, tmp_dir: str = TMP_DIR, path: str = JS_RUNTIME_PATH) -> None:
    with open(os.path.join(tmp_dir, "main.js"), "w") as fp:
        with open(os.path.join(path, "js_header")) as fq:
            fp.write(fq.read() + "\n" + solution_code + trailer_code)


def _copy_runtime_files(path: str = JS_RUNTIME_PATH, tmp_dir: str = TMP_DIR) -> None:
    for filename in JS_RUNTIME_FILES:
        src = os.path.join(path, filename)
        dst = os.path.join(tmp_dir, filename)
        shutil.copy(src, dst)


def prepare_js_workspace(solution_code: str, trailer_code: str, input_lines: List[str], tmp_dir: str = TMP_DIR) -> Tuple[int, str]:
    os.makedirs(tmp_dir, exist_ok=True)
    _write_user_input(input_lines, tmp_dir)
    _write_main_js(solution_code, trailer_code, tmp_dir=tmp_dir)
    _copy_runtime_files(tmp_dir=tmp_dir)
    return 0, ""


def run_js_workspace(tmp_dir: str = TMP_DIR) -> Tuple[int, str]:
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
        return result.returncode, result.stderr
    return 0, ""


def check_required_files(tmp_dir: str = TMP_DIR) -> Tuple[int, str]:
    required_files = ["user.out", "time_cost.txt"]
    files_in_directory = os.listdir(tmp_dir)
    missing_files = [file for file in required_files if file not in files_in_directory]
    if missing_files:
        return 1, f"Missing these files: {', '.join(missing_files)}"
    return 0, ""
