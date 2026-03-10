"""Go code generator compatibility entrypoint."""

from typing import List, Union

from utils import TypeEnum
from go_gen_common import GO_TYPE_SPECS, TIME_COST_PATH, GoMethodDef, GoClassDef
from go_gen_solution import go_generate_solution_code, go_generate_trailer_code, go_test as _go_test
from go_gen_system import go_generate_system_code, go_generate_system_trailer_code, go_system_test

__all__ = [
    "GO_TYPE_SPECS",
    "TIME_COST_PATH",
    "GoMethodDef",
    "GoClassDef",
    "go_generate_solution_code",
    "go_generate_trailer_code",
    "go_generate_system_code",
    "go_generate_system_trailer_code",
    "go_test",
    "go_system_test",
]


def go_test(
    function_name_or_method: Union[str, GoMethodDef],
    params_type: List[TypeEnum] = None,
    params_name: List[str] = None,
    return_type: TypeEnum = None,
):
    if isinstance(function_name_or_method, GoMethodDef):
        method_def = function_name_or_method
    else:
        method_def = GoMethodDef(function_name_or_method, params_type, params_name, return_type)
    return _go_test(method_def)


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
    m1 = GoMethodDef("solve", params_type, params_name, return_type)
    print_generated_code("solution", go_test(m1))

    ctor = GoMethodDef("ctor", [TypeEnum.INT], ["capacity"], TypeEnum.NONE)
    m2 = GoMethodDef("put", [TypeEnum.INT, TypeEnum.INT], ["key", "value"], TypeEnum.NONE)
    m3 = GoMethodDef("get", [TypeEnum.INT], ["key"], TypeEnum.INT)
    class_def = GoClassDef("TestSystem", ctor, [m2, m3])
    print_generated_code("system", go_system_test(class_def))
