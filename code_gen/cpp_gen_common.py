"""Shared definitions/utilities for C++ code generation."""

import os
import shutil
import subprocess
from dataclasses import dataclass
from typing import Dict, List, Tuple

from utils import TypeEnum, TypeSpec, MethodDef, ClassDef

CPP_TYPE_SPECS: Dict[TypeEnum, TypeSpec] = {
    TypeEnum.BOOL: TypeSpec("bool", "false", "des_bool", "ser_bool"),
    TypeEnum.INT: TypeSpec("int", "0", "des_int", "ser_int"),
    TypeEnum.LONG: TypeSpec("long long", "0", "des_long", "ser_long"),
    TypeEnum.DOUBLE: TypeSpec("double", "0.0", "des_double", "ser_double"),
    TypeEnum.STRING: TypeSpec("string", '""', "des_string", "ser_string"),
    TypeEnum.INT_LIST: TypeSpec("vector<int>", "vector<int>()", "des_int_list", "ser_int_list"),
    TypeEnum.INT_LIST_LIST: TypeSpec(
        "vector<vector<int>>",
        "vector<vector<int>>()",
        "des_int_list_list",
        "ser_int_list_list",
    ),
    TypeEnum.DOUBLE_LIST: TypeSpec("vector<double>", "vector<double>()", "des_double_list", "ser_double_list"),
    TypeEnum.STRING_LIST: TypeSpec("vector<string>", "vector<string>()", "des_string_list", "ser_string_list"),
    TypeEnum.BOOL_LIST: TypeSpec("vector<bool>", "vector<bool>()", "des_bool_list", "ser_bool_list"),
    TypeEnum.TREENODE: TypeSpec("TreeNode*", "nullptr", "des_tree", "ser_tree"),
    TypeEnum.LISTNODE: TypeSpec("ListNode*", "nullptr", "des_linked_list", "ser_linked_list"),
    TypeEnum.LONG_LIST: TypeSpec("vector<long long>", "vector<long long>()", "des_long_list", "ser_long_list"),
    TypeEnum.NONE: TypeSpec("void", "/*none*/", "des_none", "ser_none"),
}

TIME_COST_PATH = "time_cost.txt"
TMP_DIR = "tmp"
CPP_RUNTIME_PATH = "cpp"
CPP_RUNTIME_FILES = [
    "cpp_io_tools.h",
    "cpp_node_type.h",
    "cpp_parse_tools.h",
    "cpp_parse_module.h",
    "libcpp_parse_tools.so",
]


@dataclass
class CppMethodDef(MethodDef):
    def generate(self) -> str:
        params_list: List[str] = []
        for p_type, p_name in zip(self.params_type, self.params_name):
            t = CPP_TYPE_SPECS[p_type].lang_type
            params_list.append(f"{t} {p_name}")
        ret_type = CPP_TYPE_SPECS[self.return_type].lang_type
        signature = f"{ret_type} {self.function_name}({', '.join(params_list)})"
        return signature


@dataclass
class CppClassDef(ClassDef):
    def __post_init__(self):
        self.constructor.function_name = self.name
        self.constructor.return_type = TypeEnum.NONE

    def constructor_generate(self):
        params_list: List[str] = []
        for p_type, p_name in zip(self.constructor.params_type, self.constructor.params_name):
            t = CPP_TYPE_SPECS[p_type].lang_type
            params_list.append(f"{t} {p_name}")
        signature = f"{self.name}({', '.join(params_list)})"
        return signature


def _build_cpp_runtime_lib(path: str = CPP_RUNTIME_PATH) -> Tuple[int, str]:
    tmp_list = [
        filename
        for filename in os.listdir(path)
        if filename.startswith("libcpp_") and filename.endswith(".so")
    ]
    if tmp_list:
        return 0, ""

    result = subprocess.run(
        ["g++", "-shared", "-o", "libcpp_parse_tools.so", "-fPIC", "cpp_parse_tools.cpp", "cpp_parse_module.cpp", "../rapidjson_helper.cpp"],
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


def _write_main_cpp(solution_code: str, trailer_code: str, tmp_dir: str = TMP_DIR, path: str = CPP_RUNTIME_PATH) -> None:
    with open(os.path.join(tmp_dir, "main.cpp"), "w") as fp:
        with open(os.path.join(path, "cpp_header")) as fq:
            fp.write(fq.read() + "\n" + solution_code + trailer_code)


def _copy_runtime_files(path: str = CPP_RUNTIME_PATH, tmp_dir: str = TMP_DIR) -> None:
    for filename in CPP_RUNTIME_FILES:
        src = os.path.join(path, filename)
        dst = os.path.join(tmp_dir, filename)
        shutil.copy(src, dst)


def prepare_cpp_workspace(solution_code: str, trailer_code: str, input_lines: List[str], tmp_dir: str = TMP_DIR) -> Tuple[int, str]:
    os.makedirs(tmp_dir, exist_ok=True)
    _write_user_input(input_lines, tmp_dir)
    _write_main_cpp(solution_code, trailer_code, tmp_dir=tmp_dir)

    ret, message = _build_cpp_runtime_lib()
    if ret != 0:
        return ret, message

    _copy_runtime_files(tmp_dir=tmp_dir)
    return 0, ""


def compile_cpp_workspace(tmp_dir: str = TMP_DIR) -> Tuple[int, str]:
    result = subprocess.run(
        ["g++", "-o", "main", "main.cpp", "-L.", "-lcpp_parse_tools", "-Wl,-rpath=."],
        cwd=tmp_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        return result.returncode, result.stderr
    return 0, ""


def run_cpp_workspace(tmp_dir: str = TMP_DIR) -> Tuple[int, str]:
    result = subprocess.run(
        ["./main"],
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

