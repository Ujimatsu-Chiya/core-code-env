"""Python generator logic for system-design style problems."""

import json
import os
import shutil
from typing import List, Optional, Tuple

from utils import TypeEnum, json_default_val
from py_gen_common import (
    PY_TYPE_SPECS,
    TIME_COST_PATH,
    TMP_DIR,
    PyClassDef,
    PyMethodDef,
    prepare_py_workspace,
    run_py_workspace,
    check_required_files,
)


def py_generate_system_code(class_def: PyClassDef) -> str:
    lines = [
        f"class {class_def.name}:",
        f"    {class_def.constructor_generate()}",
        "        # write code here",
        "        pass",
        "",
    ]
    for method_def in class_def.methods:
        lines += [
            f"    {method_def.generate()}",
            "        # write code here",
            (
                "        return"
                if method_def.return_type == TypeEnum.NONE
                else f"        return {PY_TYPE_SPECS[method_def.return_type].default}"
            ),
            "",
        ]
    return "\n".join(lines)


def _py_generate_system_dispatch_block(method_defs: List[PyMethodDef], class_name: str) -> str:
    del class_name
    lines: List[str] = []
    for idx, method_def in enumerate(method_defs):
        branch = "if" if idx == 0 else "elif"
        lines.append(f'        {branch} method == "{method_def.function_name}":')
        lines.append(f"            if len(params_cur) != {len(method_def.params_type)}:")
        lines.append(f'                raise ValueError("Method `{method_def.function_name}` argument size mismatch.")')

        for p_idx, p_type in enumerate(method_def.params_type):
            spec = PY_TYPE_SPECS[p_type]
            lines.append(
                f"            p{p_idx} = {spec.des_func}(json.dumps(params_cur[{p_idx}], separators=(',', ':')))"
            )

        args = ", ".join(f"p{i}" for i in range(len(method_def.params_type)))
        lines.append("            start_stamp = time.process_time_ns()")
        if method_def.return_type == TypeEnum.NONE:
            lines.append(f"            obj.{method_def.function_name}({args})")
            lines.append("            end_stamp = time.process_time_ns()")
            lines.append("            self.ctime_total += end_stamp - start_stamp")
            lines.append("            return None")
        else:
            ret_spec = PY_TYPE_SPECS[method_def.return_type]
            lines.append(f"            ret = obj.{method_def.function_name}({args})")
            lines.append("            end_stamp = time.process_time_ns()")
            lines.append("            self.ctime_total += end_stamp - start_stamp")
            lines.append(f"            return json.loads({ret_spec.ser_func}(ret))")

    lines.append("        else:")
    lines.append('            raise ValueError("Input method does not exist.")')
    return "\n".join(lines)


def py_generate_system_trailer_code(class_def: PyClassDef) -> str:
    ctor = class_def.constructor
    ctor_param_count = len(ctor.params_type)
    ctor_parse_lines = [
        f"        if len(params[0]) != {ctor_param_count}:",
        '            raise ValueError("Constructor argument size mismatch.")',
    ]
    for idx, p_type in enumerate(ctor.params_type):
        spec = PY_TYPE_SPECS[p_type]
        ctor_parse_lines.append(
            f"        ctor_p{idx} = {spec.des_func}(json.dumps(params[0][{idx}], separators=(',', ':')))"
        )

    ctor_args = ", ".join(f"ctor_p{i}" for i in range(ctor_param_count))
    dispatch_block = _py_generate_system_dispatch_block(class_def.methods, class_def.name)

    lines = [
        "",
        "class DriverSystemSolution:",
        "    def __init__(self):",
        "        self.ctime_total = 0",
        "",
        f"    def dispatch(self, method: str, params_cur: List[Any], obj: {class_def.name}) -> Any:",
        dispatch_block,
        "",
        "    def solve(self, methods: List[str], params: List[List[Any]]) -> str:",
        "        if not methods or not params or len(methods) != len(params):",
        '            raise ValueError("Input methods size does not equal to params size or equals to 0.")',
        f'        if methods[0] != "{class_def.name}":',
        '            raise ValueError("First method is not constructor.")',
        "\n".join(ctor_parse_lines),
        "        ctor_start_stamp = time.process_time_ns()",
        f"        obj = {class_def.name}({ctor_args})",
        "        ctor_end_stamp = time.process_time_ns()",
        "        self.ctime_total += ctor_end_stamp - ctor_start_stamp",
        "",
        "        outputs: List[Any] = [None]",
        "        for i in range(1, len(methods)):",
        "            outputs.append(self.dispatch(methods[i], params[i], obj))",
        "        return json.dumps(outputs, separators=(',', ':'))",
        "",
        "",
        "def run():",
        "    reader = StdinWrapper()",
        "    writer = StdoutWrapper()",
        "    driver = DriverSystemSolution()",
        "    while True:",
        "        line_methods = reader.read_line()",
        "        if line_methods is None:",
        "            break",
        "        line_params = reader.read_line()",
        "        if line_params is None:",
        '            raise ValueError("Testcase is missing the required argument: `params`")',
        "        methods = des_string_list(line_methods)",
        "        params = json.loads(line_params)",
        "        if not isinstance(params, list):",
        '            raise ValueError("Input params must be a JSON array.")',
        "        writer.write_line(driver.solve(methods, params))",
        f'    with open("{TIME_COST_PATH}", "w") as fp:',
        '        fp.write(f"{driver.ctime_total // 1000000}")',
        "",
        'if __name__ == "__main__":',
        "    try:",
        "        run()",
        "    except Exception as e:",
        "        exc_type, exc_value, exc_traceback = sys.exc_info()",
        "        sys.stdout = sys.stderr",
        "        traceback.print_tb(exc_traceback)",
        "        traceback.print_exception(exc_type, exc_value, None)",
        "        exit(1)",
    ]

    return "\n".join(lines)


def _build_default_system_case(class_def: PyClassDef) -> Tuple[str, str, str]:
    methods = [class_def.name] + [method.function_name for method in class_def.methods]

    params = []
    ctor_values = [json.loads(json_default_val[p_type]) for p_type in class_def.constructor.params_type]
    params.append(ctor_values)
    for method in class_def.methods:
        method_values = [json.loads(json_default_val[p_type]) for p_type in method.params_type]
        params.append(method_values)

    outputs: List[object] = [None]
    for method in class_def.methods:
        if method.return_type == TypeEnum.NONE:
            outputs.append(None)
        else:
            outputs.append(json.loads(json_default_val[method.return_type]))

    methods_line = json.dumps(methods, separators=(",", ":"))
    params_line = json.dumps(params, separators=(",", ":"))
    expected_output = json.dumps(outputs, separators=(",", ":"))
    return methods_line, params_line, expected_output


def py_system_test(
    class_def: PyClassDef,
    methods_line: Optional[str] = None,
    params_line: Optional[str] = None,
    expected_output: Optional[str] = None,
):
    try:
        if methods_line is None and params_line is None and expected_output is None:
            methods_line, params_line, expected_output = _build_default_system_case(class_def)
        elif methods_line is None or params_line is None:
            return 1, "Both `methods_line` and `params_line` are required for custom testcases."

        solution_code = py_generate_system_code(class_def)
        trailer_code = py_generate_system_trailer_code(class_def)

        ret, message = prepare_py_workspace(solution_code, trailer_code, [methods_line, params_line], tmp_dir=TMP_DIR)
        if ret != 0:
            return ret, message

        ret, message = run_py_workspace(tmp_dir=TMP_DIR)
        if ret != 0:
            return ret, message

        ret, message = check_required_files(tmp_dir=TMP_DIR)
        if ret != 0:
            return ret, message

        if expected_output is not None:
            user_out_path = os.path.join(TMP_DIR, "user.out")
            with open(user_out_path, "r") as fp:
                output_lines = [line.strip() for line in fp.readlines() if line.strip()]
            if not output_lines:
                return 1, "Generated program completed but `user.out` is empty."
            if output_lines[0] != expected_output:
                return 1, f"System template output mismatch. expected={expected_output}, actual={output_lines[0]}"

        return 0, {"main_body.py": solution_code, "main_trailer.py": trailer_code}
    finally:
        shutil.rmtree(TMP_DIR, ignore_errors=True)

