"""JavaScript code generator entrypoint."""

from typing import List, Union

from code_gen.utils import TypeEnum

from .common import JS_TYPE_SPECS, TIME_COST_PATH, JsMethodDef, JsClassDef
from .solution import js_generate_solution_code, js_generate_trailer_code, js_test as _js_test
from .system import js_generate_system_code, js_generate_system_trailer_code, js_system_test

__all__ = [
    "JS_TYPE_SPECS",
    "TIME_COST_PATH",
    "JsMethodDef",
    "JsClassDef",
    "js_generate_solution_code",
    "js_generate_trailer_code",
    "js_generate_system_code",
    "js_generate_system_trailer_code",
    "js_test",
    "js_system_test",
]


def js_test(
    function_name_or_method: Union[str, JsMethodDef],
    params_type: List[TypeEnum] = None,
    params_name: List[str] = None,
    return_type: TypeEnum = None,
):
    if isinstance(function_name_or_method, JsMethodDef):
        method_def = function_name_or_method
    else:
        method_def = JsMethodDef(function_name_or_method, params_type, params_name, return_type)
    return _js_test(method_def)


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
    m1 = JsMethodDef("solve", params_type, params_name, return_type)
    print_generated_code("solution", js_test(m1))

    ctor = JsMethodDef("ctor", [TypeEnum.INT], ["capacity"], TypeEnum.NONE)
    m2 = JsMethodDef("put", [TypeEnum.INT, TypeEnum.INT], ["key", "value"], TypeEnum.NONE)
    m3 = JsMethodDef("get", [TypeEnum.INT], ["key"], TypeEnum.INT)
    class_def = JsClassDef("TestSystem", ctor, [m2, m3])
    print_generated_code("system", js_system_test(class_def))

