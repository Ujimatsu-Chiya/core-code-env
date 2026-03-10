"""Shared definitions/utilities for Go code generation."""

import os
import shutil
import subprocess
from dataclasses import dataclass
from typing import Dict, List, Tuple

from utils import TypeEnum, TypeSpec, MethodDef, ClassDef

GO_TYPE_SPECS: Dict[TypeEnum, TypeSpec] = {
    TypeEnum.BOOL: TypeSpec("bool", "false", "DesBool", "SerBool"),
    TypeEnum.INT: TypeSpec("int", "0", "DesInt", "SerInt"),
    TypeEnum.LONG: TypeSpec("int64", "0", "DesLong", "SerLong"),
    TypeEnum.DOUBLE: TypeSpec("float64", "0.0", "DesDouble", "SerDouble"),
    TypeEnum.STRING: TypeSpec("string", '""', "DesString", "SerString"),
    TypeEnum.INT_LIST: TypeSpec("[]int", "[]int{}", "DesIntList", "SerIntList"),
    TypeEnum.INT_LIST_LIST: TypeSpec("[][]int", "[][]int{}", "DesIntListList", "SerIntListList"),
    TypeEnum.DOUBLE_LIST: TypeSpec("[]float64", "[]float64{}", "DesDoubleList", "SerDoubleList"),
    TypeEnum.STRING_LIST: TypeSpec("[]string", "[]string{}", "DesStringList", "SerStringList"),
    TypeEnum.BOOL_LIST: TypeSpec("[]bool", "[]bool{}", "DesBoolList", "SerBoolList"),
    TypeEnum.TREENODE: TypeSpec("*TreeNode", "nil", "DesTree", "SerTree"),
    TypeEnum.LISTNODE: TypeSpec("*ListNode", "nil", "DesLinkedList", "SerLinkedList"),
    TypeEnum.LONG_LIST: TypeSpec("[]int64", "[]int64{}", "DesLongList", "SerLongList"),
    TypeEnum.NONE: TypeSpec("", "", "DesNone", "SerNone"),
}

TIME_COST_PATH = "time_cost.txt"
TMP_DIR = "tmp"
GO_RUNTIME_PATH = "go"
GO_RUNTIME_FILES = [
    "go_io_tools.go",
    "go_parse_tools.go",
    "go_type_node.go",
]


@dataclass
class GoMethodDef(MethodDef):
    def generate(self) -> str:
        params_list: List[str] = []
        for p_type, p_name in zip(self.params_type, self.params_name):
            params_list.append(f"{p_name} {GO_TYPE_SPECS[p_type].lang_type}")
        ret_type = GO_TYPE_SPECS[self.return_type].lang_type
        if self.return_type == TypeEnum.NONE:
            return f"func {self.function_name}({', '.join(params_list)})"
        return f"func {self.function_name}({', '.join(params_list)}) {ret_type}"


@dataclass
class GoClassDef(ClassDef):
    def __post_init__(self):
        self.constructor.function_name = f"New{self.name}"
        self.constructor.return_type = TypeEnum.NONE

    def constructor_generate(self):
        params_list: List[str] = []
        for p_type, p_name in zip(self.constructor.params_type, self.constructor.params_name):
            params_list.append(f"{p_name} {GO_TYPE_SPECS[p_type].lang_type}")
        return f"func New{self.name}({', '.join(params_list)}) *{self.name}"


def _write_user_input(input_lines: List[str], tmp_dir: str = TMP_DIR) -> None:
    with open(os.path.join(tmp_dir, "user.in"), "w") as fp:
        for line in input_lines:
            fp.write(line + "\n")


def _write_main_go(solution_code: str, trailer_code: str, tmp_dir: str = TMP_DIR, path: str = GO_RUNTIME_PATH) -> None:
    with open(os.path.join(tmp_dir, "main.go"), "w") as fp:
        with open(os.path.join(path, "go_header")) as fq:
            fp.write(fq.read() + "\n" + solution_code + trailer_code)


def _copy_runtime_files(path: str = GO_RUNTIME_PATH, tmp_dir: str = TMP_DIR) -> None:
    for filename in GO_RUNTIME_FILES:
        src = os.path.join(path, filename)
        dst = os.path.join(tmp_dir, filename)
        shutil.copy(src, dst)


def prepare_go_workspace(solution_code: str, trailer_code: str, input_lines: List[str], tmp_dir: str = TMP_DIR) -> Tuple[int, str]:
    os.makedirs(tmp_dir, exist_ok=True)
    _write_user_input(input_lines, tmp_dir)
    _write_main_go(solution_code, trailer_code, tmp_dir=tmp_dir)
    _copy_runtime_files(tmp_dir=tmp_dir)
    return 0, ""


def format_go_workspace(tmp_dir: str = TMP_DIR) -> Tuple[int, str]:
    goimports_bin = shutil.which("goimports")
    if goimports_bin is None:
        # Fallback: resolve via `go env` even when GOPATH/bin is not on PATH.
        try:
            gobin_res = subprocess.run(
                ["go", "env", "GOBIN"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            if gobin_res.returncode == 0:
                gobin = gobin_res.stdout.strip()
                if gobin:
                    candidate = os.path.join(gobin, "goimports")
                    if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
                        goimports_bin = candidate

            if goimports_bin is None:
                gopath_res = subprocess.run(
                    ["go", "env", "GOPATH"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                if gopath_res.returncode == 0:
                    for gopath in gopath_res.stdout.strip().split(os.pathsep):
                        gopath = gopath.strip()
                        if not gopath:
                            continue
                        candidate = os.path.join(gopath, "bin", "goimports")
                        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
                            goimports_bin = candidate
                            break
        except FileNotFoundError:
            pass

    if goimports_bin is None:
        return 1, "goimports is not found in PATH."

    try:
        result = subprocess.run(
            [goimports_bin, "-w", "main.go"],
            cwd=tmp_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except FileNotFoundError:
        return 1, "goimports is not found in PATH."
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip()
        return result.returncode, message
    return 0, ""


def compile_go_workspace(tmp_dir: str = TMP_DIR) -> Tuple[int, str]:
    try:
        result = subprocess.run(
            ["go", "build", "-o", "main", "main.go", "go_io_tools.go", "go_parse_tools.go", "go_type_node.go"],
            cwd=tmp_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except FileNotFoundError:
        return 1, "go is not found in PATH."
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip()
        return result.returncode, message
    return 0, ""


def run_go_workspace(tmp_dir: str = TMP_DIR) -> Tuple[int, str]:
    result = subprocess.run(
        ["./main"],
        cwd=tmp_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
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
