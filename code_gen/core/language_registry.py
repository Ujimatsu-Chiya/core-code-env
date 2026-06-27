"""Language operation registry for generator orchestration."""

from dataclasses import dataclass
from typing import Any, Callable, Dict

from code_gen.utils import to_snake_case, to_camel_case, to_pascal_case

from code_gen.languages.c.main import (
    CMethodDef,
    CClassDef,
    c_generate_solution_code,
    c_generate_trailer_code,
    c_generate_system_code,
    c_generate_system_trailer_code,
    c_test,
    c_system_test,
)
from code_gen.languages.cpp.main import (
    CppMethodDef,
    CppClassDef,
    cpp_generate_solution_code,
    cpp_generate_trailer_code,
    cpp_generate_system_code,
    cpp_generate_system_trailer_code,
    cpp_test,
    cpp_system_test,
)
from code_gen.languages.java.main import (
    JavaMethodDef,
    JavaClassDef,
    java_generate_solution_code,
    java_generate_trailer_code,
    java_generate_system_code,
    java_generate_system_trailer_code,
    java_test,
    java_system_test,
)
from code_gen.languages.py.main import (
    PyMethodDef,
    PyClassDef,
    py_generate_solution_code,
    py_generate_trailer_code,
    py_generate_system_code,
    py_generate_system_trailer_code,
    py_test,
    py_system_test,
)
from code_gen.languages.ts.main import (
    TsMethodDef,
    TsClassDef,
    ts_generate_solution_code,
    ts_generate_trailer_code,
    ts_generate_system_code,
    ts_generate_system_trailer_code,
    ts_test,
    ts_system_test,
)
from code_gen.languages.js.main import (
    JsMethodDef,
    JsClassDef,
    js_generate_solution_code,
    js_generate_trailer_code,
    js_generate_system_code,
    js_generate_system_trailer_code,
    js_test,
    js_system_test,
)
from code_gen.languages.go.main import (
    GoMethodDef,
    GoClassDef,
    go_generate_solution_code,
    go_generate_trailer_code,
    go_generate_system_code,
    go_generate_system_trailer_code,
    go_test,
    go_system_test,
)


@dataclass(frozen=True)
class SolutionLanguageOp:
    test_fn: Callable[..., Any]
    solution_fn: Callable[..., str]
    trailer_fn: Callable[..., str]
    method_cls: Any
    extension: str
    function_name_style: Callable[[str], str]
    params_name_style: Callable[[str], str]


@dataclass(frozen=True)
class SystemLanguageOp:
    system_test_fn: Callable[..., Any]
    solution_fn: Callable[..., str]
    trailer_fn: Callable[..., str]
    method_cls: Any
    class_cls: Any
    extension: str
    class_name_style: Callable[[str], str]
    method_name_style: Callable[[str], str]
    params_name_style: Callable[[str], str]


SOLUTION_LANGUAGE_OPS: Dict[str, SolutionLanguageOp] = {
    "c": SolutionLanguageOp(c_test, c_generate_solution_code, c_generate_trailer_code, CMethodDef, "c", to_snake_case, to_snake_case),
    "cpp": SolutionLanguageOp(cpp_test, cpp_generate_solution_code, cpp_generate_trailer_code, CppMethodDef, "cpp", to_snake_case, to_snake_case),
    "java": SolutionLanguageOp(java_test, java_generate_solution_code, java_generate_trailer_code, JavaMethodDef, "java", to_camel_case, to_camel_case),
    "py": SolutionLanguageOp(py_test, py_generate_solution_code, py_generate_trailer_code, PyMethodDef, "py", to_snake_case, to_snake_case),
    "ts": SolutionLanguageOp(ts_test, ts_generate_solution_code, ts_generate_trailer_code, TsMethodDef, "ts", to_camel_case, to_camel_case),
    "js": SolutionLanguageOp(js_test, js_generate_solution_code, js_generate_trailer_code, JsMethodDef, "js", to_camel_case, to_camel_case),
    "go": SolutionLanguageOp(go_test, go_generate_solution_code, go_generate_trailer_code, GoMethodDef, "go", to_pascal_case, to_camel_case),
}


SYSTEM_LANGUAGE_OPS: Dict[str, SystemLanguageOp] = {
    "c": SystemLanguageOp(c_system_test, c_generate_system_code, c_generate_system_trailer_code, CMethodDef, CClassDef, "c", to_pascal_case, to_camel_case, to_snake_case),
    "cpp": SystemLanguageOp(cpp_system_test, cpp_generate_system_code, cpp_generate_system_trailer_code, CppMethodDef, CppClassDef, "cpp", to_pascal_case, to_camel_case, to_snake_case),
    "java": SystemLanguageOp(java_system_test, java_generate_system_code, java_generate_system_trailer_code, JavaMethodDef, JavaClassDef, "java", to_pascal_case, to_camel_case, to_camel_case),
    "py": SystemLanguageOp(py_system_test, py_generate_system_code, py_generate_system_trailer_code, PyMethodDef, PyClassDef, "py", to_pascal_case, to_camel_case, to_snake_case),
    "ts": SystemLanguageOp(ts_system_test, ts_generate_system_code, ts_generate_system_trailer_code, TsMethodDef, TsClassDef, "ts", to_pascal_case, to_camel_case, to_camel_case),
    "js": SystemLanguageOp(js_system_test, js_generate_system_code, js_generate_system_trailer_code, JsMethodDef, JsClassDef, "js", to_pascal_case, to_camel_case, to_camel_case),
    "go": SystemLanguageOp(go_system_test, go_generate_system_code, go_generate_system_trailer_code, GoMethodDef, GoClassDef, "go", to_pascal_case, to_camel_case, to_camel_case),
}
