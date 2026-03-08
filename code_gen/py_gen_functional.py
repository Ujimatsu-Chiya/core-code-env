"""Python generator logic for classic function-style problems."""

import shutil

from utils import TypeEnum, json_default_val
from py_gen_common import (
    PY_TYPE_SPECS,
    TIME_COST_PATH,
    TMP_DIR,
    PyMethodDef,
    prepare_py_workspace,
    run_py_workspace,
    check_required_files,
)


def py_generate_solution_code(method_def: PyMethodDef) -> str:
    return_line = (
        "        return"
        if method_def.return_type == TypeEnum.NONE
        else f"        return {PY_TYPE_SPECS[method_def.return_type].default}"
    )
    lines = [
        "class Solution:",
        f"    {method_def.generate()}",
        "        # write code here",
        return_line,
    ]
    return "\n".join(lines)


def py_generate_trailer_code(method_def: PyMethodDef):
    params_num = len(method_def.params_name)
    lines_pre = []
    for i, (p_type, p_name) in enumerate(zip(method_def.params_type, method_def.params_name)):
        lines_pre += [
            "json_str = reader.read_line()",
            "if json_str is None:",
            "    break" if i == 0 else f'    raise ValueError("Testcase is missing the required argument: `{p_name}`")',
            f"p{i} = {PY_TYPE_SPECS[p_type].des_func}(json_str)",
        ]

    args = ", ".join(f"p{x}" for x in range(params_num))
    if method_def.return_type == TypeEnum.NONE:
        invoke_lines = [f"        Solution().{method_def.function_name}({args})"]
        output_lines = ['        writer.write_line("null")']
    else:
        invoke_lines = [f"        result = Solution().{method_def.function_name}({args})"]
        output_lines = [f"        writer.write_line({PY_TYPE_SPECS[method_def.return_type].ser_func}(result))"]

    lines = [
        "",
        "def run():",
        "    reader = StdinWrapper()",
        "    writer = StdoutWrapper()",
        "    total_time = 0",
        "",
        "    while True:",
        "\n".join([" " * 8 + s for s in lines_pre]),
        "",
        "        start_stamp = time.process_time_ns()",
        *invoke_lines,
        "        end_stamp = time.process_time_ns()",
        "        total_time += end_stamp - start_stamp",
        *output_lines,
        "",
        f'    with open("{TIME_COST_PATH}", "w") as fp:',
        '        fp.write(f"{total_time // 1000000}")',
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


def py_test(method_def: PyMethodDef):
    try:
        input_lines = [json_default_val[p_type] for p_type in method_def.params_type]
        solution_code = py_generate_solution_code(method_def)
        trailer_code = py_generate_trailer_code(method_def)

        ret, message = prepare_py_workspace(solution_code, trailer_code, input_lines, tmp_dir=TMP_DIR)
        if ret != 0:
            return ret, message

        ret, message = run_py_workspace(tmp_dir=TMP_DIR)
        if ret != 0:
            return ret, message

        ret, message = check_required_files(tmp_dir=TMP_DIR)
        if ret != 0:
            return ret, message

        return 0, {"main_body.py": solution_code, "main_trailer.py": trailer_code}
    finally:
        shutil.rmtree(TMP_DIR, ignore_errors=True)
