"""TypeScript generator logic for classic function-style problems."""

import shutil

from utils import TypeEnum, json_default_val
from ts_gen_common import (
    TS_TYPE_SPECS,
    TIME_COST_PATH,
    TMP_DIR,
    TsMethodDef,
    prepare_ts_workspace,
    compile_ts_workspace,
    run_ts_workspace,
    check_required_files,
)


def _ts_generate_driver_code(method_def: TsMethodDef) -> str:
    helper_params = ", ".join(
        f"param_{idx + 1}: {TS_TYPE_SPECS[p_type].lang_type}"
        for idx, p_type in enumerate(method_def.params_type)
    )
    helper_args = ", ".join(f"param_{idx + 1}" for idx in range(len(method_def.params_type)))
    return_type = TS_TYPE_SPECS[method_def.return_type].lang_type
    helper_signature = f"    __helper__({helper_params}): {return_type} {{"

    if method_def.return_type == TypeEnum.NONE:
        helper_body = [
            f"        new Solution().{method_def.function_name}({helper_args});",
            "        return;",
        ]
    else:
        helper_body = [
            f"        const ret: {return_type} = new Solution().{method_def.function_name}({helper_args});",
            "        return ret;",
        ]

    lines = [
        "class __DriverSolution__ {",
        helper_signature,
        *helper_body,
        "    }",
        "}",
    ]
    return "\n".join(lines)


def ts_generate_solution_code(method_def: TsMethodDef) -> str:
    return_line = (
        "        return;"
        if method_def.return_type == TypeEnum.NONE
        else f"        return {TS_TYPE_SPECS[method_def.return_type].default};"
    )
    lines = [
        "class Solution {",
        f"    {method_def.generate()} {{",
        "        // write code here",
        return_line,
        "    }",
        "}",
    ]
    return "\n".join(lines)


def ts_generate_trailer_code(method_def: TsMethodDef) -> str:
    params_num = len(method_def.params_name)
    driver_code = _ts_generate_driver_code(method_def)
    lines_pre = []
    for i, (p_type, p_name) in enumerate(zip(method_def.params_type, method_def.params_name)):
        lines_pre += [
            "jsonStr = reader.readLine();",
            "if (jsonStr === null) {",
            "    break;" if i == 0 else f'    throw new Error("Testcase is missing the required argument: `{p_name}`");',
            "}",
            f"const p{i}: {TS_TYPE_SPECS[p_type].lang_type} = TsParseTools.{TS_TYPE_SPECS[p_type].des_func}(jsonStr);",
        ]

    args = ", ".join(f"p{x}" for x in range(params_num))
    if method_def.return_type == TypeEnum.NONE:
        invoke_lines = [f"        driver.__helper__({args});"]
        output_lines = ['        writer.writeLine("null");']
    else:
        invoke_lines = [f"        const result: {TS_TYPE_SPECS[method_def.return_type].lang_type} = driver.__helper__({args});"]
        output_lines = [f"        writer.writeLine(TsParseTools.{TS_TYPE_SPECS[method_def.return_type].ser_func}(result));"]

    lines = [
        "",
        driver_code,
        "",
        "function run() {",
        "    const reader: StdinWrapper = new StdinWrapper();",
        "    const writer: StdoutWrapper = new StdoutWrapper();",
        "    const driver: __DriverSolution__ = new __DriverSolution__();",
        "    let jsonStr: string | null = null;",
        "    let totalTime = 0;",
        "",
        "    while (true) {",
        "\n".join([" " * 8 + s for s in lines_pre]),
        "",
        "        const startStamp = process.hrtime.bigint();",
        *invoke_lines,
        "        const endStamp = process.hrtime.bigint();",
        "        totalTime += Number(endStamp - startStamp);",
        *output_lines,
        "    }",
        "",
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


def ts_test(method_def: TsMethodDef):
    try:
        input_lines = [json_default_val[p_type] for p_type in method_def.params_type]
        solution_code = ts_generate_solution_code(method_def)
        trailer_code = ts_generate_trailer_code(method_def)

        ret, message = prepare_ts_workspace(solution_code, trailer_code, input_lines, tmp_dir=TMP_DIR)
        if ret != 0:
            return ret, message

        ret, message = compile_ts_workspace(tmp_dir=TMP_DIR)
        if ret != 0:
            return ret, message

        ret, message = run_ts_workspace(tmp_dir=TMP_DIR)
        if ret != 0:
            return ret, message

        ret, message = check_required_files(tmp_dir=TMP_DIR)
        if ret != 0:
            return ret, message

        return 0, {"main_body.ts": solution_code, "main_trailer.ts": trailer_code}
    finally:
        shutil.rmtree(TMP_DIR, ignore_errors=True)

