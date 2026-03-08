"""Shared definitions/utilities for Python code generation."""

import os
import shutil
import subprocess
from dataclasses import dataclass
from typing import Dict, List, Tuple

from utils import TypeEnum, TypeSpec, MethodDef, ClassDef

PY_TYPE_SPECS: Dict[TypeEnum, TypeSpec] = {
    TypeEnum.BOOL: TypeSpec("bool", "False", "des_bool", "ser_bool"),
    TypeEnum.INT: TypeSpec("int", "0", "des_int", "ser_int"),
    TypeEnum.LONG: TypeSpec("int", "0", "des_long", "ser_long"),
    TypeEnum.DOUBLE: TypeSpec("float", "0.0", "des_double", "ser_double"),
    TypeEnum.STRING: TypeSpec("str", '""', "des_string", "ser_string"),
    TypeEnum.INT_LIST: TypeSpec("List[int]", "[]", "des_int_list", "ser_int_list"),
    TypeEnum.INT_LIST_LIST: TypeSpec("List[List[int]]", "[]", "des_int_list_list", "ser_int_list_list"),
    TypeEnum.DOUBLE_LIST: TypeSpec("List[float]", "[]", "des_double_list", "ser_double_list"),
    TypeEnum.STRING_LIST: TypeSpec("List[str]", "[]", "des_string_list", "ser_string_list"),
    TypeEnum.BOOL_LIST: TypeSpec("List[bool]", "[]", "des_bool_list", "ser_bool_list"),
    TypeEnum.TREENODE: TypeSpec("TreeNode", "None", "des_tree", "ser_tree"),
    TypeEnum.LISTNODE: TypeSpec("ListNode", "None", "des_linked_list", "ser_linked_list"),
    TypeEnum.LONG_LIST: TypeSpec("List[int]", "[]", "des_long_list", "ser_long_list"),
    TypeEnum.NONE: TypeSpec("None", "None", "des_none", "ser_none"),
}

TIME_COST_PATH = "time_cost.txt"
TMP_DIR = "tmp"
PY_RUNTIME_PATH = "python3"


@dataclass
class PyMethodDef(MethodDef):
    def generate(self) -> str:
        params_list: List[str] = []
        for p_type, p_name in zip(self.params_type, self.params_name):
            p_type_str = PY_TYPE_SPECS[p_type].lang_type
            params_list.append(f"{p_name}: {p_type_str}")
        if params_list:
            args = ", " + ", ".join(params_list)
        else:
            args = ""
        py_signature = f"def {self.function_name}(self{args}) -> {PY_TYPE_SPECS[self.return_type].lang_type}:"
        return py_signature


@dataclass
class PyClassDef(ClassDef):
    def __post_init__(self):
        self.constructor.function_name = "__init__"
        self.constructor.return_type = TypeEnum.NONE

    def constructor_generate(self):
        return self.constructor.generate()


def _build_py_runtime_module(path: str = PY_RUNTIME_PATH) -> Tuple[int, str]:
    so_files = [filename for filename in os.listdir(path) if filename.startswith("py") and filename.endswith(".so")]
    if so_files:
        return 0, ""

    result = subprocess.run(
        ["python3", "setup.py", "build", "--build-lib", "."],
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


def _write_main_py(solution_code: str, trailer_code: str, tmp_dir: str = TMP_DIR, path: str = PY_RUNTIME_PATH) -> None:
    with open(os.path.join(tmp_dir, "main.py"), "w") as fp:
        with open(os.path.join(path, "py_header")) as fq:
            fp.write(fq.read() + "\n" + solution_code + trailer_code)


def _copy_runtime_files(path: str = PY_RUNTIME_PATH, tmp_dir: str = TMP_DIR) -> None:
    for filename in os.listdir(path):
        if filename.startswith("py") and (filename.endswith(".py") or filename.endswith(".so")):
            src = os.path.join(path, filename)
            dst = os.path.join(tmp_dir, filename)
            shutil.copy(src, dst)


def prepare_py_workspace(solution_code: str, trailer_code: str, input_lines: List[str], tmp_dir: str = TMP_DIR) -> Tuple[int, str]:
    os.makedirs(tmp_dir, exist_ok=True)
    _write_user_input(input_lines, tmp_dir)
    _write_main_py(solution_code, trailer_code, tmp_dir=tmp_dir)

    ret, message = _build_py_runtime_module()
    if ret != 0:
        return ret, message

    _copy_runtime_files(tmp_dir=tmp_dir)
    return 0, ""


def run_py_workspace(tmp_dir: str = TMP_DIR) -> Tuple[int, str]:
    result = subprocess.run(
        ["python3", "main.py"],
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

