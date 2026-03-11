"""Python generator logic for system-design style problems."""

from typing import List, Optional

from code_gen.utils import TypeEnum
from code_gen.core.workspace import create_tmp_workspace, cleanup_tmp_workspace
from code_gen.core.system_test_utils import (
    default_output_from_json_default,
    resolve_system_case_inputs,
    verify_expected_user_output,
)

from .common import (
    PY_TYPE_SPECS,
    TIME_COST_PATH,
    PyClassDef,
    PyMethodDef,
    prepare_py_workspace,
    run_py_workspace,
    check_required_files,
)


def _generate_api_usage_comment(class_def: PyClassDef) -> str:
    ctor_args = ", ".join(class_def.constructor.params_name)
    lines = [
        f"# Your {class_def.name} object will be instantiated and called as such:",
        f"# obj = {class_def.name}({ctor_args})",
    ]
    for idx, method in enumerate(class_def.methods, start=1):
        m_args = ", ".join(method.params_name)
        if method.return_type == TypeEnum.NONE:
            lines.append(f"# obj.{method.function_name}({m_args})")
        else:
            lines.append(f"# result_{idx} = obj.{method.function_name}({m_args})")
    return "\n".join(lines)


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
    lines += [
        "",
        _generate_api_usage_comment(class_def),
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


def py_system_test(
    class_def: PyClassDef,
    methods_line: Optional[str] = None,
    params_line: Optional[str] = None,
    expected_output: Optional[str] = None,
):
    tmp_dir = create_tmp_workspace("code_gen_py_")
    try:
        ret, payload = resolve_system_case_inputs(
            class_def,
            methods_line,
            params_line,
            expected_output,
            output_value_builder=default_output_from_json_default,
        )
        if ret != 0:
            return ret, payload
        methods_line, params_line, expected_output = payload

        solution_code = py_generate_system_code(class_def)
        trailer_code = py_generate_system_trailer_code(class_def)

        ret, message = prepare_py_workspace(solution_code, trailer_code, [methods_line, params_line], tmp_dir=tmp_dir)
        if ret != 0:
            return ret, message

        ret, message = run_py_workspace(tmp_dir=tmp_dir)
        if ret != 0:
            return ret, message

        ret, message = check_required_files(tmp_dir=tmp_dir)
        if ret != 0:
            return ret, message

        error = verify_expected_user_output(tmp_dir, expected_output)
        if error is not None:
            return 1, error

        return 0, {"main_body.py": solution_code, "main_trailer.py": trailer_code}
    finally:
        cleanup_tmp_workspace(tmp_dir)
