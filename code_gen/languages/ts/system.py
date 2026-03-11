"""TypeScript generator logic for system-design style problems."""

from typing import List, Optional, Tuple

from code_gen.utils import TypeEnum
from code_gen.core.workspace import create_tmp_workspace, cleanup_tmp_workspace
from code_gen.core.system_test_utils import (
    default_output_from_json_default,
    resolve_system_case_inputs,
    verify_expected_user_output,
)
from .common import (
    TS_TYPE_SPECS,
    TIME_COST_PATH,
    TsClassDef,
    TsMethodDef,
    prepare_ts_workspace,
    compile_ts_workspace,
    run_ts_workspace,
    check_required_files,
)


def _generate_api_usage_comment(class_def: TsClassDef) -> str:
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
            lines.append(
                f" * const result_{idx}: {TS_TYPE_SPECS[method.return_type].lang_type} = obj.{method.function_name}({m_args});"
            )
    lines += [" */"]
    return "\n".join(lines)


def ts_generate_system_code(class_def: TsClassDef) -> str:
    lines = [
        f"class {class_def.name} {{",
        f"    {class_def.constructor_generate()} {{",
        "        // write code here",
        "    }",
        "",
    ]
    for method_def in class_def.methods:
        lines += [
            f"    {method_def.generate()} {{",
            "        // write code here",
            (
                "        return;"
                if method_def.return_type == TypeEnum.NONE
                else f"        return {TS_TYPE_SPECS[method_def.return_type].default};"
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


def _ts_generate_system_dispatch_block(method_defs: List[TsMethodDef]) -> str:
    lines: List[str] = []
    for idx, method_def in enumerate(method_defs):
        branch = "if" if idx == 0 else "else if"
        lines.append(f'        {branch} (method === "{method_def.function_name}") {{')
        lines.append(f"            if (paramsCur.length !== {len(method_def.params_type)}) {{")
        lines.append(f'                throw new Error("Method `{method_def.function_name}` argument size mismatch.");')
        lines.append("            }")

        for p_idx, p_type in enumerate(method_def.params_type):
            spec = TS_TYPE_SPECS[p_type]
            lines.append(
                f"            const p{p_idx}: {spec.lang_type} = TsParseTools.{spec.des_func}(JSON.stringify(paramsCur[{p_idx}]));"
            )

        args = ", ".join(f"p{i}" for i in range(len(method_def.params_type)))
        lines.append("            const startStamp = process.hrtime.bigint();")
        if method_def.return_type == TypeEnum.NONE:
            lines.append(f"            obj.{method_def.function_name}({args});")
            lines.append("            const endStamp = process.hrtime.bigint();")
            lines.append("            this.ctimeTotal += Number(endStamp - startStamp);")
            lines.append("            return null;")
        else:
            ret_spec = TS_TYPE_SPECS[method_def.return_type]
            lines.append(f"            const ret: {ret_spec.lang_type} = obj.{method_def.function_name}({args});")
            lines.append("            const endStamp = process.hrtime.bigint();")
            lines.append("            this.ctimeTotal += Number(endStamp - startStamp);")
            lines.append(f"            return JSON.parse(TsParseTools.{ret_spec.ser_func}(ret));")
        lines.append("        }")

    lines.append("        else {")
    lines.append('            throw new Error("Input method does not exist.");')
    lines.append("        }")
    return "\n".join(lines)


def ts_generate_system_trailer_code(class_def: TsClassDef) -> str:
    ctor = class_def.constructor
    ctor_param_count = len(ctor.params_type)
    ctor_parse_lines = [
        f"        if (params[0].length !== {ctor_param_count}) {{",
        '            throw new Error("Constructor argument size mismatch.");',
        "        }",
    ]
    for idx, p_type in enumerate(ctor.params_type):
        spec = TS_TYPE_SPECS[p_type]
        ctor_parse_lines.append(
            f"        const ctorP{idx}: {spec.lang_type} = TsParseTools.{spec.des_func}(JSON.stringify(params[0][{idx}]));"
        )

    ctor_args = ", ".join(f"ctorP{i}" for i in range(ctor_param_count))
    dispatch_block = _ts_generate_system_dispatch_block(class_def.methods)

    lines = [
        "",
        "class DriverSystemSolution {",
        "    ctimeTotal = 0;",
        "",
        f"    dispatch(method: string, paramsCur: any[], obj: {class_def.name}): any {{",
        dispatch_block,
        "    }",
        "",
        "    solve(methods: string[], params: any[][]): string {",
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
        "        const outputs: any[] = [null];",
        "        for (let i = 1; i < methods.length; i++) {",
        "            outputs.push(this.dispatch(methods[i], params[i], obj));",
        "        }",
        "        return JSON.stringify(outputs);",
        "    }",
        "}",
        "",
        "function run() {",
        "    const reader: StdinWrapper = new StdinWrapper();",
        "    const writer: StdoutWrapper = new StdoutWrapper();",
        "    const driver = new DriverSystemSolution();",
        "    while (true) {",
        "        const lineMethods = reader.readLine();",
        "        if (lineMethods === null) {",
        "            break;",
        "        }",
        "        const lineParams = reader.readLine();",
        "        if (lineParams === null) {",
        '            throw new Error("Testcase is missing the required argument: `params`");',
        "        }",
        "        const methods: string[] = TsParseTools.desStringList(lineMethods);",
        "        const paramsRaw = JSON.parse(lineParams);",
        "        if (!Array.isArray(paramsRaw)) {",
        '            throw new Error("Input params must be a JSON array.");',
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


def ts_system_test(
    class_def: TsClassDef,
    methods_line: Optional[str] = None,
    params_line: Optional[str] = None,
    expected_output: Optional[str] = None,
):
    tmp_dir = create_tmp_workspace("code_gen_ts_")
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

        solution_code = ts_generate_system_code(class_def)
        trailer_code = ts_generate_system_trailer_code(class_def)

        ret, message = prepare_ts_workspace(solution_code, trailer_code, [methods_line, params_line], tmp_dir=tmp_dir)
        if ret != 0:
            return ret, message

        ret, message = compile_ts_workspace(tmp_dir=tmp_dir)
        if ret != 0:
            return ret, message

        ret, message = run_ts_workspace(tmp_dir=tmp_dir)
        if ret != 0:
            return ret, message

        ret, message = check_required_files(tmp_dir=tmp_dir)
        if ret != 0:
            return ret, message

        error = verify_expected_user_output(tmp_dir, expected_output)
        if error is not None:
            return 1, error

        return 0, {"main_body.ts": solution_code, "main_trailer.ts": trailer_code}
    finally:
        cleanup_tmp_workspace(tmp_dir)
