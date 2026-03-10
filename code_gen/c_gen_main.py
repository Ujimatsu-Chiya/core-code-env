"""C code generator compatibility entrypoint."""

from typing import List, Union

from utils import TypeEnum
from c_gen_common import C_TYPE_SPECS, TIME_COST_PATH, CMethodDef, CClassDef
from c_gen_solution import c_generate_solution_code, c_generate_trailer_code, c_test as _c_test
from c_gen_system import c_generate_system_code, c_generate_system_trailer_code, c_system_test

__all__ = [
    "C_TYPE_SPECS",
    "TIME_COST_PATH",
    "CMethodDef",
    "CClassDef",
    "c_generate_solution_code",
    "c_generate_trailer_code",
    "c_generate_system_code",
    "c_generate_system_trailer_code",
    "c_test",
    "c_system_test",
]


def c_test(
    function_name_or_method: Union[str, CMethodDef],
    params_type: List[TypeEnum] = None,
    params_name: List[str] = None,
    return_type: TypeEnum = None,
):
    if isinstance(function_name_or_method, CMethodDef):
        method_def = function_name_or_method
    else:
        method_def = CMethodDef(function_name_or_method, params_type, params_name, return_type)
    return _c_test(method_def)


if __name__ == "__main__":
    def print_generated_code(test_name, test_result):
        ret, payload = test_result
        if ret != 0:
            print(f"[{test_name}] failed: {payload}")
            return
        for filename, code in payload.items():
            print(f"===== {test_name} / {filename} =====")
            print(code)

    params_type = [
        TypeEnum.INT,
        TypeEnum.LONG,
        TypeEnum.DOUBLE,
        TypeEnum.STRING,
        TypeEnum.INT_LIST,
        TypeEnum.INT_LIST_LIST,
        TypeEnum.DOUBLE_LIST,
        TypeEnum.STRING_LIST,
        TypeEnum.BOOL_LIST,
        TypeEnum.BOOL,
        TypeEnum.TREENODE,
        TypeEnum.LISTNODE,
    ]
    params_name = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l"]
    return_type = TypeEnum.INT_LIST_LIST
    m1 = CMethodDef("solve", params_type, params_name, return_type)
    print_generated_code("solution", c_test(m1))

    ctor = CMethodDef("ctor", [TypeEnum.INT], ["capacity"], TypeEnum.NONE)
    m2 = CMethodDef("push", [TypeEnum.INT], ["x"], TypeEnum.NONE)
    m3 = CMethodDef("pop", [], [], TypeEnum.NONE)
    m4 = CMethodDef("top", [], [], TypeEnum.INT)
    m5 = CMethodDef("getMin", [], [], TypeEnum.INT)
    class_def = CClassDef("MinStack", ctor, [m2, m3, m4, m5])
    print_generated_code("system", c_system_test(class_def))
