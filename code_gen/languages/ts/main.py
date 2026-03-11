"""TypeScript code generator entrypoint."""

from typing import List, Union

from code_gen.utils import TypeEnum

from .common import TS_TYPE_SPECS, TIME_COST_PATH, TsMethodDef, TsClassDef
from .solution import ts_generate_solution_code, ts_generate_trailer_code, ts_test as _ts_test
from .system import ts_generate_system_code, ts_generate_system_trailer_code, ts_system_test

__all__ = [
    "TS_TYPE_SPECS",
    "TIME_COST_PATH",
    "TsMethodDef",
    "TsClassDef",
    "ts_generate_solution_code",
    "ts_generate_trailer_code",
    "ts_generate_system_code",
    "ts_generate_system_trailer_code",
    "ts_test",
    "ts_system_test",
]


def ts_test(
    function_name_or_method: Union[str, TsMethodDef],
    params_type: List[TypeEnum] = None,
    params_name: List[str] = None,
    return_type: TypeEnum = None,
):
    if isinstance(function_name_or_method, TsMethodDef):
        method_def = function_name_or_method
    else:
        method_def = TsMethodDef(function_name_or_method, params_type, params_name, return_type)
    return _ts_test(method_def)


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
    m1 = TsMethodDef("solve", params_type, params_name, return_type)
    print_generated_code("solution", ts_test(m1))

    ctor = TsMethodDef("ctor", [TypeEnum.INT], ["capacity"], TypeEnum.NONE)
    m2 = TsMethodDef("put", [TypeEnum.INT, TypeEnum.INT], ["key", "value"], TypeEnum.NONE)
    m3 = TsMethodDef("get", [TypeEnum.INT], ["key"], TypeEnum.INT)
    class_def = TsClassDef("TestSystem", ctor, [m2, m3])
    print_generated_code("system", ts_system_test(class_def))

