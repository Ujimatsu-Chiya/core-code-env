"""JavaScript generator logic for system-design style problems."""

import json
import os
import shutil
from typing import List, Optional, Tuple

from utils import TypeEnum, json_default_val
from js_gen_common import (
    JS_TYPE_SPECS,
    TIME_COST_PATH,
    TMP_DIR,
    JsClassDef,
    JsMethodDef,
    prepare_js_workspace,
    run_js_workspace,
    check_required_files,
)


def _generate_api_usage_comment(class_def: JsClassDef) -> str:
    ctor_args = ", ".join(class_def.constructor.params_name)
    lines = [
        "/**",
        f" * Your {class_def.name} object will be instantiated and called as such:",
        f" * const obj = new {class_def.name}({ctor_args});",
    ]
    for idx, method in enumerate(class_def.methods, start=1):
        m_args = ", ".join(method.params_name)
        if method.return_type == TypeEnum.NONE:
            lines.append(f" * obj.{method.function_name}({m_args});")
        else:
            lines.append(f" * const result_{idx} = obj.{method.function_name}({m_args});")
    lines += [" */"]
    return "\n".join(lines)


def js_generate_system_code(class_def: JsClassDef) -> str:
    ctor_doc = [
        "    /**",
        *[
            f"     * @param {{{JS_TYPE_SPECS[p_type].lang_type}}} {p_name}"
            for p_type, p_name in zip(class_def.constructor.params_type, class_def.constructor.params_name)
        ],
        "    */",
    ]
    lines = [
        f"class {class_def.name} {{",
        *ctor_doc,
        f"    {class_def.constructor_generate()} {{",
        "        // write code here",
        "    }",
        "",
    ]
    for method_def in class_def.methods:
        method_doc = [
            "    /**",
            *[
                f"     * @param {{{JS_TYPE_SPECS[p_type].lang_type}}} {p_name}"
                for p_type, p_name in zip(method_def.params_type, method_def.params_name)
            ],
            f"     * @return {{{JS_TYPE_SPECS[method_def.return_type].lang_type}}}",
            "    */",
        ]
        lines += [
            *method_doc,
            f"    {method_def.generate()} {{",
            "        // write code here",
            (
                "        return;"
                if method_def.return_type == TypeEnum.NONE
                else f"        return {JS_TYPE_SPECS[method_def.return_type].default};"
            ),
            "    }",
            "",
        ]
    lines += [
        "}",
        "",
        _generate_api_usage_comment(class_def),
    ]
    return "\n".join(lines)


def _js_generate_system_dispatch_block(method_defs: List[JsMethodDef]) -> str:
    lines: List[str] = []
    for idx, method_def in enumerate(method_defs):
        branch = "if" if idx == 0 else "else if"
        lines.append(f'        {branch} (method === "{method_def.function_name}") {{')
        lines.append(f"            if (paramsCur.length !== {len(method_def.params_type)}) {{")
        lines.append(f'                throw new Error("Method `{method_def.function_name}` argument size mismatch.");')
        lines.append("            }")

        for p_idx, p_type in enumerate(method_def.params_type):
            spec = JS_TYPE_SPECS[p_type]
            lines.append(
                f"            const p{p_idx} = JsParseTools.{spec.des_func}(JSON.stringify(paramsCur[{p_idx}]));"
            )

        args = ", ".join(f"p{i}" for i in range(len(method_def.params_type)))
        lines.append("            const startStamp = process.hrtime.bigint();")
        if method_def.return_type == TypeEnum.NONE:
            lines.append(f"            obj.{method_def.function_name}({args});")
            lines.append("            const endStamp = process.hrtime.bigint();")
            lines.append("            this.ctimeTotal += Number(endStamp - startStamp);")
            lines.append("            return null;")
        else:
            ret_spec = JS_TYPE_SPECS[method_def.return_type]
            lines.append(f"            const ret = obj.{method_def.function_name}({args});")
            lines.append("            const endStamp = process.hrtime.bigint();")
            lines.append("            this.ctimeTotal += Number(endStamp - startStamp);")
            lines.append(f"            return JSON.parse(JsParseTools.{ret_spec.ser_func}(ret));")
        lines.append("        }")

    lines.append("        else {")
    lines.append('            throw new Error("Input method does not exist.");')
    lines.append("        }")
    return "\n".join(lines)


def js_generate_system_trailer_code(class_def: JsClassDef) -> str:
    ctor = class_def.constructor
    ctor_param_count = len(ctor.params_type)
    ctor_parse_lines = [
        f"        if (params[0].length !== {ctor_param_count}) {{",
        '            throw new Error("Constructor argument size mismatch.");',
        "        }",
    ]
    for idx, p_type in enumerate(ctor.params_type):
        spec = JS_TYPE_SPECS[p_type]
        ctor_parse_lines.append(
            f"        const ctorP{idx} = JsParseTools.{spec.des_func}(JSON.stringify(params[0][{idx}]));"
        )

    ctor_args = ", ".join(f"ctorP{i}" for i in range(ctor_param_count))
    dispatch_block = _js_generate_system_dispatch_block(class_def.methods)

    lines = [
        "",
        "class DriverSystemSolution {",
        "    constructor() {",
        "        this.ctimeTotal = 0;",
        "    }",
        "",
        f"    dispatch(method, paramsCur, obj) {{",
        dispatch_block,
        "    }",
        "",
        "    solve(methods, params) {",
        "        if (methods.length === 0 || params.length === 0 || methods.length !== params.length) {",
        '            throw new Error("Input methods size does not equal to params size or equals to 0.");',
        "        }",
        f'        if (methods[0] !== "{class_def.name}") {{',
        '            throw new Error("First method is not constructor.");',
        "        }",
        "\n".join(ctor_parse_lines),
        "        const ctorStartStamp = process.hrtime.bigint();",
        f"        const obj = new {class_def.name}({ctor_args});",
        "        const ctorEndStamp = process.hrtime.bigint();",
        "        this.ctimeTotal += Number(ctorEndStamp - ctorStartStamp);",
        "",
        "        const outputs = [null];",
        "        for (let i = 1; i < methods.length; i++) {",
        "            outputs.push(this.dispatch(methods[i], params[i], obj));",
        "        }",
        "        return JSON.stringify(outputs);",
        "    }",
        "}",
        "",
        "function run() {",
        "    const reader = new JsIoTools.StdinWrapper();",
        "    const writer = new JsIoTools.StdoutWrapper();",
        "    const driver = new DriverSystemSolution();",
        "    while (true) {",
        "        const lineMethods = reader.readLine();",
        "        if (lineMethods === null) {",
        "            break;",
        "        }",
        "        const lineParams = reader.readLine();",
        "        if (lineParams === null) {",
        '            throw new Error(\"Testcase is missing the required argument: `params`\");',
        "        }",
        "        const methods = JsParseTools.desStringList(lineMethods);",
        "        const paramsRaw = JSON.parse(lineParams);",
        "        if (!Array.isArray(paramsRaw)) {",
        '            throw new Error(\"Input params must be a JSON array.\");',
        "        }",
        "        writer.writeLine(driver.solve(methods, paramsRaw));",
        "    }",
        f'    fs.writeFileSync("{TIME_COST_PATH}", Math.floor(driver.ctimeTotal / 1000000).toString());',
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


def _build_default_system_case(class_def: JsClassDef) -> Tuple[str, str, str]:
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


def js_system_test(
    class_def: JsClassDef,
    methods_line: Optional[str] = None,
    params_line: Optional[str] = None,
    expected_output: Optional[str] = None,
):
    try:
        if methods_line is None and params_line is None and expected_output is None:
            methods_line, params_line, expected_output = _build_default_system_case(class_def)
        elif methods_line is None or params_line is None:
            return 1, "Both `methods_line` and `params_line` are required for custom testcases."

        solution_code = js_generate_system_code(class_def)
        trailer_code = js_generate_system_trailer_code(class_def)

        ret, message = prepare_js_workspace(solution_code, trailer_code, [methods_line, params_line], tmp_dir=TMP_DIR)
        if ret != 0:
            return ret, message

        ret, message = run_js_workspace(tmp_dir=TMP_DIR)
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

        return 0, {"main_body.js": solution_code, "main_trailer.js": trailer_code}
    finally:
        shutil.rmtree(TMP_DIR, ignore_errors=True)
