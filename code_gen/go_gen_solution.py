"""Go generator logic for classic function-style problems."""

import shutil

from utils import TypeEnum, json_default_val
from go_gen_common import (
    GO_TYPE_SPECS,
    TIME_COST_PATH,
    TMP_DIR,
    GoMethodDef,
    prepare_go_workspace,
    format_go_workspace,
    compile_go_workspace,
    run_go_workspace,
    check_required_files,
)


def _go_generate_driver_code(method_def: GoMethodDef) -> str:
    helper_params = ", ".join(
        f"param_{idx + 1} {GO_TYPE_SPECS[p_type].lang_type}"
        for idx, p_type in enumerate(method_def.params_type)
    )
    helper_args = ", ".join(f"param_{idx + 1}" for idx in range(len(method_def.params_type)))
    return_type = GO_TYPE_SPECS[method_def.return_type].lang_type

    if method_def.return_type == TypeEnum.NONE:
        signature = f"func (d *__DriverSolution__) __helper__({helper_params})"
        helper_body = [
            f"    {method_def.function_name}({helper_args})",
            "    return",
        ]
    else:
        signature = f"func (d *__DriverSolution__) __helper__({helper_params}) {return_type}"
        helper_body = [
            f"    ret := {method_def.function_name}({helper_args})",
            "    return ret",
        ]

    lines = [
        "type __DriverSolution__ struct {}",
        "",
        f"{signature} {{",
        *helper_body,
        "}",
    ]
    return "\n".join(lines)


def go_generate_solution_code(method_def: GoMethodDef) -> str:
    return_line = (
        "    return"
        if method_def.return_type == TypeEnum.NONE
        else f"    return {GO_TYPE_SPECS[method_def.return_type].default}"
    )
    lines = [
        "",
        f"{method_def.generate()} {{",
        "    // write code here",
        return_line,
        "}",
    ]
    return "\n".join(lines)


def go_generate_trailer_code(method_def: GoMethodDef) -> str:
    params_num = len(method_def.params_name)
    driver_code = _go_generate_driver_code(method_def)
    lines_pre = []
    for i, (p_type, p_name) in enumerate(zip(method_def.params_type, method_def.params_name)):
        lines_pre += [
            f'jsonStr {":=" if i == 0 else "="} reader.ReadLine()',
            "if jsonStr == \"\" {",
            "    break" if i == 0 else f'    fmt.Fprintf(os.Stderr, "Testcase is missing the required argument: `{p_name}`")',
            "" if i == 0 else "    os.Exit(1)",
            "}",
            f"p{i} := {GO_TYPE_SPECS[p_type].des_func}(jsonStr)",
        ]
    lines_pre = [line for line in lines_pre if line != ""]

    args = ", ".join(f"p{x}" for x in range(params_num))
    if method_def.return_type == TypeEnum.NONE:
        invoke_lines = [f"        driver.__helper__({args})"]
        output_lines = ['        writer.WriteLine("null")']
    else:
        invoke_lines = [f"        result := driver.__helper__({args})"]
        output_lines = [f"        writer.WriteLine({GO_TYPE_SPECS[method_def.return_type].ser_func}(result))"]

    lines = [
        "",
        driver_code,
        "",
        "func Run() {",
        "    reader := CreateStdinWrapper()",
        "    writer := CreateStdoutWrapper()",
        "    driver := &__DriverSolution__{}",
        "    totalTime := int64(0)",
        "    for {",
        "\n".join([" " * 8 + s for s in lines_pre]),
        "",
        "        startStamp := GetCPUTime()",
        *invoke_lines,
        "        endStamp := GetCPUTime()",
        "        totalTime += endStamp - startStamp",
        *output_lines,
        "    }",
        f'    timeCostFile, err := os.Create("{TIME_COST_PATH}")',
        "    if err != nil {",
        '        fmt.Fprintf(os.Stderr, "Error creating time cost file: %v", err)',
        "        os.Exit(1)",
        "    }",
        '    fmt.Fprintf(timeCostFile, "%d", totalTime / 1000000)',
        "}",
        "",
        "func main() {",
        "    Run()",
        "}",
    ]
    return "\n".join(lines)


def go_test(method_def: GoMethodDef):
    try:
        input_lines = [json_default_val[p_type] for p_type in method_def.params_type]
        solution_code = go_generate_solution_code(method_def)
        trailer_code = go_generate_trailer_code(method_def)

        ret, message = prepare_go_workspace(solution_code, trailer_code, input_lines, tmp_dir=TMP_DIR)
        if ret != 0:
            return ret, message

        ret, message = format_go_workspace(tmp_dir=TMP_DIR)
        if ret != 0:
            return ret, message

        ret, message = compile_go_workspace(tmp_dir=TMP_DIR)
        if ret != 0:
            return ret, message

        ret, message = run_go_workspace(tmp_dir=TMP_DIR)
        if ret != 0:
            return ret, message

        ret, message = check_required_files(tmp_dir=TMP_DIR)
        if ret != 0:
            return ret, message

        return 0, {"main_body.go": solution_code, "main_trailer.go": trailer_code}
    finally:
        shutil.rmtree(TMP_DIR, ignore_errors=True)

