"""Cross-language generation orchestration."""

import os
from typing import Dict, List

from code_gen.utils import TypeEnum, MethodDef
from code_gen.core.language_registry import SOLUTION_LANGUAGE_OPS, SYSTEM_LANGUAGE_OPS


def _clean_generated_outputs(result_dir: str) -> None:
    os.makedirs(result_dir, exist_ok=True)

    # Clean previously generated files in target directory.
    for filename in os.listdir(result_dir):
        if not (filename.startswith("main_body.") or filename.startswith("main_trailer.")):
            continue
        file_path = os.path.join(result_dir, filename)
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
            except FileNotFoundError:
                # Another parallel run may have already removed it.
                pass


def _save_payload(result_dir: str, payload: Dict[str, str]) -> None:
    os.makedirs(result_dir, exist_ok=True)
    for filename, code in payload.items():
        with open(os.path.join(result_dir, filename), "w") as fp:
            fp.write(code)


def test_solution(
    function_name: str,
    params_type: List[TypeEnum],
    params_name: List[str],
    return_type: TypeEnum,
    result_dir: str = "result/solution",
):
    assert len(params_name) == len(params_type)
    _clean_generated_outputs(result_dir)
    all_results = {}
    for lang, op in SOLUTION_LANGUAGE_OPS.items():
        styled_fn = op.function_name_style(function_name)
        styled_params = list(map(op.params_name_style, params_name))
        method_def = op.method_cls(styled_fn, params_type, styled_params, return_type)
        result = op.test_fn(method_def)
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

    all_results = {}
    for lang, op in SYSTEM_LANGUAGE_OPS.items():
        styled_class_name = op.class_name_style(class_name)
        ctor = op.method_cls(
            "ctor",
            constructor_params_type,
            list(map(op.params_name_style, constructor_params_name)),
            TypeEnum.NONE,
        )
        styled_methods = []
        for method in methods:
            styled_methods.append(
                op.method_cls(
                    op.method_name_style(method.function_name),
                    method.params_type,
                    list(map(op.params_name_style, method.params_name)),
                    method.return_type,
                )
            )
        class_def = op.class_cls(styled_class_name, ctor, styled_methods)
        result = op.system_test_fn(class_def)
        if result[0] != 0:
            print(f"[{lang}] {result}")
            all_results[lang] = result
            continue
        payload = result[1]
        _save_payload(result_dir, payload)
        all_results[lang] = (0, sorted(payload.keys()))
    return all_results


def main() -> None:
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

    methods = [
        MethodDef("push", [TypeEnum.INT], ["x"], TypeEnum.NONE),
        MethodDef("pop", [], [], TypeEnum.NONE),
        MethodDef("top", [], [], TypeEnum.INT),
        MethodDef("getMin", [], [], TypeEnum.INT),
    ]
    print(test_system("MinStack", [TypeEnum.INT], ["capacity"], methods))


__all__ = [
    "test_solution",
    "test_system",
    "main",
]
