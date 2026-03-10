"""JavaScript generator logic for classic function-style problems."""

import shutil

from utils import TypeEnum, json_default_val
from js_gen_common import (
    JS_TYPE_SPECS,
    TIME_COST_PATH,
    TMP_DIR,
    JsMethodDef,
    prepare_js_workspace,
    run_js_workspace,
    check_required_files,
)


def _js_generate_driver_code(method_def: JsMethodDef) -> str:
    helper_params = ", ".join(f"param_{idx + 1}" for idx in range(len(method_def.params_type)))
    helper_args = ", ".join(f"param_{idx + 1}" for idx in range(len(method_def.params_type)))

    if method_def.return_type == TypeEnum.NONE:
        helper_body = [
            f"        new Solution().{method_def.function_name}({helper_args});",
            "        return;",
        ]
    else:
        helper_body = [
            f"        const ret = new Solution().{method_def.function_name}({helper_args});",
            "        return ret;",
        ]

    lines = [
        "class __DriverSolution__ {",
        f"    __helper__({helper_params}) {{",
        *helper_body,
        "    }",
        "}",
    ]
    return "\n".join(lines)


def _build_solution_doc(method_def: JsMethodDef) -> str:
    lines = ["/**"]
    for p_type, p_name in zip(method_def.params_type, method_def.params_name):
        lines.append(f" * @param {{{JS_TYPE_SPECS[p_type].lang_type}}} {p_name}")
    lines.append(f" * @return {{{JS_TYPE_SPECS[method_def.return_type].lang_type}}}")
    lines.append(" */")
    return "\n".join(lines)


def js_generate_solution_code(method_def: JsMethodDef) -> str:
    return_line = (
        "        return;"
        if method_def.return_type == TypeEnum.NONE
        else f"        return {JS_TYPE_SPECS[method_def.return_type].default};"
    )
    lines = [
        "class Solution {",
        _build_solution_doc(method_def),
        f"    {method_def.generate()} {{",
        "        // write code here",
        return_line,
        "    }",
        "}",
    ]
    return "\n".join(lines)


def js_generate_trailer_code(method_def: JsMethodDef) -> str:
    params_num = len(method_def.params_name)
    driver_code = _js_generate_driver_code(method_def)
    lines_pre = []
    for i, (p_type, p_name) in enumerate(zip(method_def.params_type, method_def.params_name)):
        lines_pre += [
            "jsonStr = reader.readLine();",
            "if (jsonStr === null) {",
            "    break;" if i == 0 else f'    throw new Error("Testcase is missing the required argument: `{p_name}`");',
            "}",
            f"const p{i} = JsParseTools.{JS_TYPE_SPECS[p_type].des_func}(jsonStr);",
        ]

    args = ", ".join(f"p{x}" for x in range(params_num))
    if method_def.return_type == TypeEnum.NONE:
        invoke_lines = [f"        driver.__helper__({args});"]
        output_lines = ['        writer.writeLine("null");']
    else:
        invoke_lines = [f"        const result = driver.__helper__({args});"]
        output_lines = [f"        writer.writeLine(JsParseTools.{JS_TYPE_SPECS[method_def.return_type].ser_func}(result));"]

    lines = [
        "",
        driver_code,
        "",
        "function run() {",
        "    const reader = new JsIoTools.StdinWrapper();",
        "    const writer = new JsIoTools.StdoutWrapper();",
        "    const driver = new __DriverSolution__();",
        "    let jsonStr = null;",
        "    let totalTime = 0;",
        "    while (true) {",
        "\n".join([" " * 8 + s for s in lines_pre]),
        "",
        "        const startStamp = process.hrtime.bigint();",
        *invoke_lines,
        "        const endStamp = process.hrtime.bigint();",
        "        totalTime += Number(endStamp - startStamp);",
        *output_lines,
        "    }",
        f'    fs.writeFileSync("{TIME_COST_PATH}", Math.floor(totalTime / 1000000).toString());',
        "}",
        "",
        "try {",
        "    run();",
        "} catch (e) {",
        "    console.error(e);",
        "    process.exit(1);",
        "}",
    ]
    return "\n".join(lines)


def js_test(method_def: JsMethodDef):
    try:
        input_lines = [json_default_val[p_type] for p_type in method_def.params_type]
        solution_code = js_generate_solution_code(method_def)
        trailer_code = js_generate_trailer_code(method_def)

        ret, message = prepare_js_workspace(solution_code, trailer_code, input_lines, tmp_dir=TMP_DIR)
        if ret != 0:
            return ret, message

        ret, message = run_js_workspace(tmp_dir=TMP_DIR)
        if ret != 0:
            return ret, message

        ret, message = check_required_files(tmp_dir=TMP_DIR)
        if ret != 0:
            return ret, message

        return 0, {"main_body.js": solution_code, "main_trailer.js": trailer_code}
    finally:
        shutil.rmtree(TMP_DIR, ignore_errors=True)

