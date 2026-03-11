"""Shared definitions/utilities for C code generation."""

import os
import shutil
import subprocess
from dataclasses import dataclass
from typing import Dict, List, Tuple

from code_gen.utils import (
    TypeEnum,
    TypeSpec,
    MethodDef,
    ClassDef,
    to_camel_case,
    to_pascal_case,
)
from code_gen.runtime_layout import get_runtime_path, get_rapidjson_helper_cpp

C_TYPE_SPECS: Dict[TypeEnum, TypeSpec] = {
    TypeEnum.BOOL: TypeSpec("bool", "false", "des_bool", "ser_bool"),
    TypeEnum.INT: TypeSpec("int", "0", "des_int", "ser_int"),
    TypeEnum.LONG: TypeSpec("long long", "0", "des_long", "ser_long"),
    TypeEnum.DOUBLE: TypeSpec("double", "0.0", "des_double", "ser_double"),
    TypeEnum.STRING: TypeSpec("char*", "NULL", "des_string", "ser_string"),
    TypeEnum.INT_LIST: TypeSpec("int*", "NULL", "des_int_list", "ser_int_list"),
    TypeEnum.INT_LIST_LIST: TypeSpec("int**", "NULL", "des_int_list_list", "ser_int_list_list"),
    TypeEnum.DOUBLE_LIST: TypeSpec("double*", "NULL", "des_double_list", "ser_double_list"),
    TypeEnum.STRING_LIST: TypeSpec("char**", "NULL", "des_string_list", "ser_string_list"),
    TypeEnum.BOOL_LIST: TypeSpec("bool*", "NULL", "des_bool_list", "ser_bool_list"),
    TypeEnum.TREENODE: TypeSpec("struct TreeNode*", "NULL", "des_tree", "ser_tree"),
    TypeEnum.LISTNODE: TypeSpec("struct ListNode*", "NULL", "des_linked_list", "ser_linked_list"),
    TypeEnum.LONG_LIST: TypeSpec("long long*", "NULL", "des_long_list", "ser_long_list"),
    TypeEnum.NONE: TypeSpec("void", "/*none*/", "des_none", "ser_none"),
}

C_DELETE_FUNC = {
    TypeEnum.STRING: "delete_string",
    TypeEnum.INT_LIST: "delete_int_list",
    TypeEnum.INT_LIST_LIST: "delete_int_list_list",
    TypeEnum.DOUBLE_LIST: "delete_double_list",
    TypeEnum.STRING_LIST: "delete_string_list",
    TypeEnum.BOOL_LIST: "delete_bool_list",
    TypeEnum.TREENODE: "delete_tree",
    TypeEnum.LISTNODE: "delete_linked_list",
    TypeEnum.LONG_LIST: "delete_long_list",
}

TIME_COST_PATH = "time_cost.txt"
TMP_DIR = "tmp"
C_RUNTIME_PATH = get_runtime_path("c")
C_RUNTIME_FILES = [
    "c_io_tools.h",
    "c_io_tools.c",
    "c_node_type.h",
    "c_parse_tools.h",
    "c_parse_module.h",
    "libc_parse_tools.so",
]


def _c_param_decl(p_type: TypeEnum, p_name: str) -> List[str]:
    decls = [f"{C_TYPE_SPECS[p_type].lang_type} {p_name}"]
    dim = TypeEnum.get_dimension(p_type)
    if dim == 1:
        decls.append(f"size_t {p_name}_size")
    elif dim == 2:
        decls.append(f"size_t {p_name}_rows")
        decls.append(f"size_t* {p_name}_cols")
    return decls


def _c_return_aux_params(return_type: TypeEnum) -> List[str]:
    dim = TypeEnum.get_dimension(return_type)
    if dim == 1:
        return ["size_t* result_size"]
    if dim == 2:
        return ["size_t* result_rows", "size_t** result_cols"]
    return []


def _c_call_args_for_param(p_type: TypeEnum, var_name: str) -> List[str]:
    dim = TypeEnum.get_dimension(p_type)
    if dim == 0:
        return [var_name]
    if dim == 1:
        return [var_name, f"{var_name}_size"]
    return [var_name, f"{var_name}_rows", f"{var_name}_cols"]


def _c_return_call_args(return_type: TypeEnum) -> List[str]:
    dim = TypeEnum.get_dimension(return_type)
    if dim == 1:
        return ["&result_size"]
    if dim == 2:
        return ["&result_rows", "&result_cols"]
    return []


def _c_return_aux_decl_lines(return_type: TypeEnum) -> List[str]:
    dim = TypeEnum.get_dimension(return_type)
    if dim == 1:
        return ["size_t result_size = 0;"]
    if dim == 2:
        return ["size_t result_rows = 0;", "size_t* result_cols = NULL;"]
    return []


def _c_cleanup_lines(p_type: TypeEnum, var_name: str) -> List[str]:
    if p_type not in C_DELETE_FUNC:
        return []
    dim = TypeEnum.get_dimension(p_type)
    func = C_DELETE_FUNC[p_type]
    if dim == 0:
        return [f"{func}({var_name});"]
    if dim == 1:
        if p_type == TypeEnum.STRING_LIST:
            return [f"{func}({var_name}, {var_name}_size);"]
        return [f"{func}({var_name});"]
    return [f"{func}({var_name}, {var_name}_rows);", f"delete_size_t_list({var_name}_cols);"]


def generate_c_signature(
    function_name: str,
    params_type: List[TypeEnum],
    params_name: List[str],
    return_type: TypeEnum,
    obj_type: str = "",
) -> str:
    params_list: List[str] = []
    if obj_type:
        params_list.append(f"{obj_type}* obj")
    for p_type, p_name in zip(params_type, params_name):
        params_list.extend(_c_param_decl(p_type, p_name))
    params_list.extend(_c_return_aux_params(return_type))
    return f"{C_TYPE_SPECS[return_type].lang_type} {function_name}({', '.join(params_list)})"


@dataclass
class CMethodDef(MethodDef):
    def generate(self) -> str:
        return generate_c_signature(self.function_name, self.params_type, self.params_name, self.return_type)


@dataclass
class CClassDef(ClassDef):
    def __post_init__(self):
        pass

    @property
    def prefix(self) -> str:
        return to_camel_case(self.name)

    def constructor_c_name(self) -> str:
        return f"{self.prefix}Create"

    def destructor_c_name(self) -> str:
        return f"{self.prefix}Free"

    def method_c_name(self, method: CMethodDef) -> str:
        return f"{self.prefix}{to_pascal_case(method.function_name)}"

    def constructor_generate(self):
        return build_c_constructor_signature_for_system(self)


def build_c_method_signature_for_system(class_def: CClassDef, method_def: CMethodDef) -> str:
    return generate_c_signature(
        class_def.method_c_name(method_def),
        method_def.params_type,
        method_def.params_name,
        method_def.return_type,
        obj_type=class_def.name,
    )


def build_c_constructor_signature_for_system(class_def: CClassDef) -> str:
    params_list: List[str] = []
    for p_type, p_name in zip(class_def.constructor.params_type, class_def.constructor.params_name):
        params_list.extend(_c_param_decl(p_type, p_name))
    return f"{class_def.name}* {class_def.constructor_c_name()}({', '.join(params_list)})"


def build_c_destructor_signature_for_system(class_def: CClassDef) -> str:
    return f"void {class_def.destructor_c_name()}({class_def.name}* obj)"


def _build_c_runtime_lib(path: str = C_RUNTIME_PATH) -> Tuple[int, str]:
    so_files = [filename for filename in os.listdir(path) if filename.startswith("libc_") and filename.endswith(".so")]
    if so_files:
        return 0, ""

    result = subprocess.run(
        [
            "g++",
            "-shared",
            "-o",
            "libc_parse_tools.so",
            "-fPIC",
            "c_parse_tools.c",
            "c_parse_module.cpp",
            get_rapidjson_helper_cpp(),
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


def _write_main_c(solution_code: str, trailer_code: str, tmp_dir: str = TMP_DIR, path: str = C_RUNTIME_PATH) -> None:
    with open(os.path.join(tmp_dir, "main.c"), "w") as fp:
        with open(os.path.join(path, "c_header")) as fq:
            fp.write(fq.read() + "\n" + solution_code + trailer_code)


def _copy_runtime_files(path: str = C_RUNTIME_PATH, tmp_dir: str = TMP_DIR) -> None:
    for filename in C_RUNTIME_FILES:
        src = os.path.join(path, filename)
        dst = os.path.join(tmp_dir, filename)
        shutil.copy(src, dst)


def prepare_c_workspace(solution_code: str, trailer_code: str, input_lines: List[str], tmp_dir: str = TMP_DIR) -> Tuple[int, str]:
    os.makedirs(tmp_dir, exist_ok=True)
    _write_user_input(input_lines, tmp_dir)
    _write_main_c(solution_code, trailer_code, tmp_dir=tmp_dir)

    ret, message = _build_c_runtime_lib()
    if ret != 0:
        return ret, message

    _copy_runtime_files(tmp_dir=tmp_dir)
    return 0, ""


def compile_c_workspace(tmp_dir: str = TMP_DIR) -> Tuple[int, str]:
    result = subprocess.run(
        ["gcc", "-o", "main", "main.c", "c_io_tools.c", "-L.", "-lc_parse_tools", "-Wl,-rpath=."],
        cwd=tmp_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        return result.returncode, result.stderr
    return 0, ""


def run_c_workspace(tmp_dir: str = TMP_DIR) -> Tuple[int, str]:
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


__all__ = [
    "C_TYPE_SPECS",
    "C_DELETE_FUNC",
    "TIME_COST_PATH",
    "TMP_DIR",
    "CMethodDef",
    "CClassDef",
    "generate_c_signature",
    "build_c_method_signature_for_system",
    "build_c_constructor_signature_for_system",
    "build_c_destructor_signature_for_system",
    "_c_call_args_for_param",
    "_c_return_call_args",
    "_c_return_aux_decl_lines",
    "_c_cleanup_lines",
    "prepare_c_workspace",
    "compile_c_workspace",
    "run_c_workspace",
    "check_required_files",
]
