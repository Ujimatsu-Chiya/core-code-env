"""Shared helpers for system-template tests."""

import json
import os
from typing import Any, Callable, Optional, Tuple

from code_gen.utils import TypeEnum, json_default_val


def default_output_from_json_default(return_type: TypeEnum) -> Any:
    if return_type == TypeEnum.NONE:
        return None
    return json.loads(json_default_val[return_type])


def build_default_system_case(
    class_def: Any,
    output_value_builder: Callable[[TypeEnum], Any] = default_output_from_json_default,
) -> Tuple[str, str, str]:
    methods = [class_def.name] + [method.function_name for method in class_def.methods]

    params = []
    ctor_values = [json.loads(json_default_val[p_type]) for p_type in class_def.constructor.params_type]
    params.append(ctor_values)
    for method in class_def.methods:
        method_values = [json.loads(json_default_val[p_type]) for p_type in method.params_type]
        params.append(method_values)

    outputs = [None]
    for method in class_def.methods:
        outputs.append(output_value_builder(method.return_type))

    methods_line = json.dumps(methods, separators=(",", ":"))
    params_line = json.dumps(params, separators=(",", ":"))
    expected_output = json.dumps(outputs, separators=(",", ":"))
    return methods_line, params_line, expected_output


def resolve_system_case_inputs(
    class_def: Any,
    methods_line: Optional[str],
    params_line: Optional[str],
    expected_output: Optional[str],
    output_value_builder: Callable[[TypeEnum], Any] = default_output_from_json_default,
) -> Tuple[int, Any]:
    if methods_line is None and params_line is None and expected_output is None:
        return 0, build_default_system_case(class_def, output_value_builder)
    if methods_line is None or params_line is None:
        return 1, "Both `methods_line` and `params_line` are required for custom testcases."
    return 0, (methods_line, params_line, expected_output)


def verify_expected_user_output(tmp_dir: str, expected_output: Optional[str]) -> Optional[str]:
    if expected_output is None:
        return None

    user_out_path = os.path.join(tmp_dir, "user.out")
    with open(user_out_path, "r") as fp:
        output_lines = [line.strip() for line in fp.readlines() if line.strip()]
    if not output_lines:
        return "Generated program completed but `user.out` is empty."
    if output_lines[0] != expected_output:
        return f"System template output mismatch. expected={expected_output}, actual={output_lines[0]}"
    return None
