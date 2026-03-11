"""Language operation registry for generator test orchestration."""

from dataclasses import dataclass
from typing import Any, Callable, Dict

from code_gen.utils import to_snake_case, to_camel_case, to_pascal_case

from code_gen.languages.c.main import CMethodDef, CClassDef, c_test, c_system_test
from code_gen.languages.cpp.main import CppMethodDef, CppClassDef, cpp_test, cpp_system_test
from code_gen.languages.java.main import JavaMethodDef, JavaClassDef, java_test, java_system_test
from code_gen.languages.py.main import PyMethodDef, PyClassDef, py_test, py_system_test
from code_gen.languages.ts.main import TsMethodDef, TsClassDef, ts_test, ts_system_test
from code_gen.languages.js.main import JsMethodDef, JsClassDef, js_test, js_system_test
from code_gen.languages.go.main import GoMethodDef, GoClassDef, go_test, go_system_test


@dataclass(frozen=True)
class SolutionLanguageOp:
    test_fn: Callable[..., Any]
    method_cls: Any
    function_name_style: Callable[[str], str]
    params_name_style: Callable[[str], str]


@dataclass(frozen=True)
class SystemLanguageOp:
    system_test_fn: Callable[..., Any]
    method_cls: Any
    class_cls: Any
    class_name_style: Callable[[str], str]
    method_name_style: Callable[[str], str]
    params_name_style: Callable[[str], str]


SOLUTION_LANGUAGE_OPS: Dict[str, SolutionLanguageOp] = {
    "c": SolutionLanguageOp(c_test, CMethodDef, to_snake_case, to_snake_case),
    "cpp": SolutionLanguageOp(cpp_test, CppMethodDef, to_snake_case, to_snake_case),
    "java": SolutionLanguageOp(java_test, JavaMethodDef, to_camel_case, to_camel_case),
    "py": SolutionLanguageOp(py_test, PyMethodDef, to_snake_case, to_snake_case),
    "ts": SolutionLanguageOp(ts_test, TsMethodDef, to_camel_case, to_camel_case),
    "js": SolutionLanguageOp(js_test, JsMethodDef, to_camel_case, to_camel_case),
    "go": SolutionLanguageOp(go_test, GoMethodDef, to_pascal_case, to_camel_case),
}


SYSTEM_LANGUAGE_OPS: Dict[str, SystemLanguageOp] = {
    "c": SystemLanguageOp(c_system_test, CMethodDef, CClassDef, to_pascal_case, to_camel_case, to_snake_case),
    "cpp": SystemLanguageOp(cpp_system_test, CppMethodDef, CppClassDef, to_pascal_case, to_camel_case, to_snake_case),
    "java": SystemLanguageOp(java_system_test, JavaMethodDef, JavaClassDef, to_pascal_case, to_camel_case, to_camel_case),
    "py": SystemLanguageOp(py_system_test, PyMethodDef, PyClassDef, to_pascal_case, to_camel_case, to_snake_case),
    "ts": SystemLanguageOp(ts_system_test, TsMethodDef, TsClassDef, to_pascal_case, to_camel_case, to_camel_case),
    "js": SystemLanguageOp(js_system_test, JsMethodDef, JsClassDef, to_pascal_case, to_camel_case, to_camel_case),
    "go": SystemLanguageOp(go_system_test, GoMethodDef, GoClassDef, to_pascal_case, to_camel_case, to_camel_case),
}
