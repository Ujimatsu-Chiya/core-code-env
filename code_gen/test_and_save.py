import os
from typing import Callable, Dict, List, Tuple

from utils import *

from c_gen_main import CMethodDef, CClassDef, c_test, c_system_test
from cpp_gen_main import CppMethodDef, CppClassDef, cpp_test, cpp_system_test
from java_gen_main import JavaMethodDef, JavaClassDef, java_test, java_system_test
from py_gen_main import PyMethodDef, PyClassDef, py_test, py_system_test
from ts_gen_main import TsMethodDef, TsClassDef, ts_test, ts_system_test
from js_gen_main import JsMethodDef, JsClassDef, js_test, js_system_test
from go_gen_main import GoMethodDef, GoClassDef, go_test, go_system_test


def _clean_generated_outputs(result_dir: str) -> None:
    os.makedirs(result_dir, exist_ok=True)

    # Clean previously generated files in target directory.
    for filename in os.listdir(result_dir):
        if not (filename.startswith("main_body.") or filename.startswith("main_trailer.")):
            continue
        file_path = os.path.join(result_dir, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    # Also clean legacy root-level artifacts under ./result.
    parent_dir = os.path.dirname(result_dir.rstrip("/"))
    if parent_dir and os.path.basename(parent_dir) == "result" and os.path.isdir(parent_dir):
        for filename in os.listdir(parent_dir):
            if not (filename.startswith("main_body.") or filename.startswith("main_trailer.")):
                continue
            file_path = os.path.join(parent_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)


def _save_payload(result_dir: str, payload: Dict[str, str]) -> None:
    os.makedirs(result_dir, exist_ok=True)
    for filename, code in payload.items():
        with open(os.path.join(result_dir, filename), "w") as fp:
            fp.write(code)


def test_solution(function_name: str, params_type: List[TypeEnum], params_name: List[str], return_type: TypeEnum, result_dir: str = "result/solution"):
    assert len(params_name) == len(params_type)
    _clean_generated_outputs(result_dir)
    operations = {
        "c": (c_test, CMethodDef, to_snake_case, to_snake_case),
        "cpp": (cpp_test, CppMethodDef, to_snake_case, to_snake_case),
        "java": (java_test, JavaMethodDef, to_camel_case, to_camel_case),
        "py": (py_test, PyMethodDef, to_snake_case, to_snake_case),
        "ts": (ts_test, TsMethodDef, to_camel_case, to_camel_case),
        "js": (js_test, JsMethodDef, to_camel_case, to_camel_case),
        "go": (go_test, GoMethodDef, to_pascal_case, to_camel_case),
    }
    all_results = {}
    for lang, (lang_test, method_cls, function_name_style, params_name_style) in operations.items():
        styled_fn = function_name_style(function_name)
        styled_params = list(map(params_name_style, params_name))
        method_def = method_cls(styled_fn, params_type, styled_params, return_type)
        result = lang_test(method_def)
        if result[0] != 0:
            print(f"[{lang}] {result}")
            all_results[lang] = result
            continue
        payload = result[1]
        _save_payload(result_dir, payload)
        all_results[lang] = (0, sorted(payload.keys()))
    return all_results


def test_system(
    class_name: str,
    constructor_params_type: List[TypeEnum],
    constructor_params_name: List[str],
    methods: List[MethodDef],
    result_dir: str = "result/system",
):
    assert len(constructor_params_name) == len(constructor_params_type)
    _clean_generated_outputs(result_dir)
    for method in methods:
        assert len(method.params_name) == len(method.params_type)

    operations = {
        "c": (c_system_test, CMethodDef, CClassDef, to_pascal_case, to_camel_case, to_snake_case),
        "cpp": (cpp_system_test, CppMethodDef, CppClassDef, to_pascal_case, to_camel_case, to_snake_case),
        "java": (java_system_test, JavaMethodDef, JavaClassDef, to_pascal_case, to_camel_case, to_camel_case),
        "py": (py_system_test, PyMethodDef, PyClassDef, to_pascal_case, to_camel_case, to_snake_case),
        "ts": (ts_system_test, TsMethodDef, TsClassDef, to_pascal_case, to_camel_case, to_camel_case),
        "js": (js_system_test, JsMethodDef, JsClassDef, to_pascal_case, to_camel_case, to_camel_case),
        "go": (go_system_test, GoMethodDef, GoClassDef, to_pascal_case, to_camel_case, to_camel_case),
    }
    all_results = {}
    for lang, (
        lang_system_test,
        method_cls,
        class_cls,
        class_name_style,
        method_name_style,
        params_name_style,
    ) in operations.items():
        styled_class_name = class_name_style(class_name)
        ctor = method_cls(
            "ctor",
            constructor_params_type,
            list(map(params_name_style, constructor_params_name)),
            TypeEnum.NONE,
        )
        styled_methods = []
        for method in methods:
            styled_methods.append(
                method_cls(
                    method_name_style(method.function_name),
                    method.params_type,
                    list(map(params_name_style, method.params_name)),
                    method.return_type,
                )
            )
        class_def = class_cls(styled_class_name, ctor, styled_methods)
        result = lang_system_test(class_def)
        if result[0] != 0:
            print(f"[{lang}] {result}")
            all_results[lang] = result
            continue
        payload = result[1]
        _save_payload(result_dir, payload)
        all_results[lang] = (0, sorted(payload.keys()))
    return all_results


# Backward-compatible alias.
def test(function_name: str, params_type: List[TypeEnum], params_name: List[str], return_type: TypeEnum):
    return test_solution(function_name, params_type, params_name, return_type)


if __name__ == "__main__":
    # Function-style template generation.
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
    params_name = [
        "appleTreeInTheMorning",
        "bigMountainWithSnow",
        "coolBreezeOnTheBeach",
        "dancingStarsUnderTheMoonlight",
        "elegantFlowerInTheGarden",
        "funnyDogChasingItsTail",
        "greenAppleFreshFromTheTree",
        "happyBirdSingingInTheTree",
        "interestingBookWithManyStories",
        "joyfulSunriseOnTheHorizon",
        "kindHeartHelpingOthers",
        "laughingChildInThePark",
    ]
    print(test_solution("solve", params_type, params_name, TypeEnum.INT_LIST_LIST))

    # System-design template generation.
    methods = [
        MethodDef("push", [TypeEnum.INT], ["x"], TypeEnum.NONE),
        MethodDef("pop", [], [], TypeEnum.NONE),
        MethodDef("top", [], [], TypeEnum.INT),
        MethodDef("getMin", [], [], TypeEnum.INT),
    ]
    print(test_system("MinStack", [TypeEnum.INT], ["capacity"], methods))
