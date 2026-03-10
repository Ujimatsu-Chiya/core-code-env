"""Go generator logic for system-design style problems."""

import json
import os
import shutil
from typing import List, Optional, Tuple

from utils import TypeEnum, json_default_val
from go_gen_common import (
    GO_TYPE_SPECS,
    TIME_COST_PATH,
    TMP_DIR,
    GoClassDef,
    GoMethodDef,
    prepare_go_workspace,
    format_go_workspace,
    compile_go_workspace,
    run_go_workspace,
    check_required_files,
)


def _generate_api_usage_comment(class_def: GoClassDef) -> str:
    ctor_args = ", ".join(class_def.constructor.params_name)
    lines = [
        "/*",
        f" * Your {class_def.name} object will be instantiated and called as such:",
        f" * obj := New{class_def.name}({ctor_args})",
    ]
    for idx, method in enumerate(class_def.methods, start=1):
        m_args = ", ".join(method.params_name)
        if method.return_type == TypeEnum.NONE:
            lines.append(f" * obj.{method.function_name}({m_args})")
        else:
            lines.append(f" * result_{idx} := obj.{method.function_name}({m_args})")
    lines += [" */"]
    return "\n".join(lines)


def _go_generate_method_with_receiver(method_def: GoMethodDef, class_name: str) -> str:
    params_list: List[str] = []
    for p_type, p_name in zip(method_def.params_type, method_def.params_name):
        params_list.append(f"{p_name} {GO_TYPE_SPECS[p_type].lang_type}")
    if method_def.return_type == TypeEnum.NONE:
        return f"func (this *{class_name}) {method_def.function_name}({', '.join(params_list)})"
    return_type = GO_TYPE_SPECS[method_def.return_type].lang_type
    return f"func (this *{class_name}) {method_def.function_name}({', '.join(params_list)}) {return_type}"


def go_generate_system_code(class_def: GoClassDef) -> str:
    lines = [
        "",
        f"type {class_def.name} struct {{",
        "    // write code here",
        "}",
        "",
        f"{class_def.constructor_generate()} {{",
        "    // write code here",
        f"    return &{class_def.name}{{}}",
        "}",
        "",
    ]
    for method_def in class_def.methods:
        lines += [
            f"{_go_generate_method_with_receiver(method_def, class_def.name)} {{",
            "    // write code here",
            (
                "    return"
                if method_def.return_type == TypeEnum.NONE
                else f"    return {GO_TYPE_SPECS[method_def.return_type].default}"
            ),
            "}",
            "",
        ]
    lines += [
        _generate_api_usage_comment(class_def),
    ]
    return "\n".join(lines)


def _go_generate_system_dispatch_block(method_defs: List[GoMethodDef]) -> str:
    lines: List[str] = []
    for method_def in method_defs:
        lines.append(f'    if method == "{method_def.function_name}" {{')
        lines.append(f"        if len(paramsCur) != {len(method_def.params_type)} {{")
        lines.append(f'            fmt.Fprintf(os.Stderr, "Method `{method_def.function_name}` argument size mismatch.")')
        lines.append("            os.Exit(1)")
        lines.append("        }")

        for p_idx, p_type in enumerate(method_def.params_type):
            spec = GO_TYPE_SPECS[p_type]
            lines.append(f"        p{p_idx} := {spec.des_func}(string(paramsCur[{p_idx}]))")

        args = ", ".join(f"p{i}" for i in range(len(method_def.params_type)))
        lines.append("        startStamp := GetCPUTime()")
        if method_def.return_type == TypeEnum.NONE:
            lines.append(f"        obj.{method_def.function_name}({args})")
            lines.append("        endStamp := GetCPUTime()")
            lines.append("        d.ctimeTotal += endStamp - startStamp")
            lines.append('        return "null"')
        else:
            ret_spec = GO_TYPE_SPECS[method_def.return_type]
            lines.append(f"        ret := obj.{method_def.function_name}({args})")
            lines.append("        endStamp := GetCPUTime()")
            lines.append("        d.ctimeTotal += endStamp - startStamp")
            lines.append(f"        return {ret_spec.ser_func}(ret)")
        lines.append("    }")
        lines.append("")

    lines.append('    fmt.Fprintf(os.Stderr, "Input method does not exist.")')
    lines.append("    os.Exit(1)")
    lines.append('    return ""')
    return "\n".join(lines)


def go_generate_system_trailer_code(class_def: GoClassDef) -> str:
    ctor = class_def.constructor
    ctor_param_count = len(ctor.params_type)
    ctor_parse_lines = [
        f"    if len(params[0]) != {ctor_param_count} {{",
        '        fmt.Fprintf(os.Stderr, "Constructor argument size mismatch.")',
        "        os.Exit(1)",
        "    }",
    ]
    for idx, p_type in enumerate(ctor.params_type):
        spec = GO_TYPE_SPECS[p_type]
        ctor_parse_lines.append(f"    ctorP{idx} := {spec.des_func}(string(params[0][{idx}]))")

    ctor_args = ", ".join(f"ctorP{i}" for i in range(ctor_param_count))
    dispatch_block = _go_generate_system_dispatch_block(class_def.methods)

    lines = [
        "",
        "type DriverSystemSolution struct {",
        "    ctimeTotal int64",
        "}",
        "",
        f"func (d *DriverSystemSolution) dispatch(method string, paramsCur []json.RawMessage, obj *{class_def.name}) string {{",
        dispatch_block,
        "}",
        "",
        "func (d *DriverSystemSolution) solve(methods []string, params [][]json.RawMessage) string {",
        "    if len(methods) == 0 || len(params) == 0 || len(methods) != len(params) {",
        '        fmt.Fprintf(os.Stderr, "Input methods size does not equal to params size or equals to 0.")',
        "        os.Exit(1)",
        "    }",
        f'    if methods[0] != "{class_def.name}" {{',
        '        fmt.Fprintf(os.Stderr, "First method is not constructor.")',
        "        os.Exit(1)",
        "    }",
        "\n".join(ctor_parse_lines),
        "    ctorStartStamp := GetCPUTime()",
        f"    obj := New{class_def.name}({ctor_args})",
        "    ctorEndStamp := GetCPUTime()",
        "    d.ctimeTotal += ctorEndStamp - ctorStartStamp",
        "",
        '    outputs := []json.RawMessage{json.RawMessage("null")}',
        "    for i := 1; i < len(methods); i++ {",
        "        outputJson := d.dispatch(methods[i], params[i], obj)",
        "        outputs = append(outputs, json.RawMessage(outputJson))",
        "    }",
        "    outputBytes, err := json.Marshal(outputs)",
        "    if err != nil {",
        '        fmt.Fprintf(os.Stderr, "Error during Serialization: %v\\n", err)',
        "        os.Exit(1)",
        "    }",
        "    return string(outputBytes)",
        "}",
        "",
        "func Run() {",
        "    reader := CreateStdinWrapper()",
        "    writer := CreateStdoutWrapper()",
        "    driver := &DriverSystemSolution{}",
        "    for {",
        "        lineMethods := reader.ReadLine()",
        '        if lineMethods == "" {',
        "            break",
        "        }",
        "        lineParams := reader.ReadLine()",
        '        if lineParams == "" {',
        '            fmt.Fprintf(os.Stderr, "Testcase is missing the required argument: `params`")',
        "            os.Exit(1)",
        "        }",
        "        methods := DesStringList(lineMethods)",
        "        var params [][]json.RawMessage",
        "        err := json.Unmarshal([]byte(lineParams), &params)",
        "        if err != nil {",
        '            fmt.Fprintf(os.Stderr, "Error during Deserialization: %v\\n", err)',
        "            os.Exit(1)",
        "        }",
        "        writer.WriteLine(driver.solve(methods, params))",
        "    }",
        f'    timeCostFile, err := os.Create("{TIME_COST_PATH}")',
        "    if err != nil {",
        '        fmt.Fprintf(os.Stderr, "Error creating time cost file: %v", err)',
        "        os.Exit(1)",
        "    }",
        '    fmt.Fprintf(timeCostFile, "%d", driver.ctimeTotal/1000000)',
        "}",
        "",
        "func main() {",
        "    Run()",
        "}",
    ]
    return "\n".join(lines)


def _build_default_system_case(class_def: GoClassDef) -> Tuple[str, str, str]:
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


def go_system_test(
    class_def: GoClassDef,
    methods_line: Optional[str] = None,
    params_line: Optional[str] = None,
    expected_output: Optional[str] = None,
):
    try:
        if methods_line is None and params_line is None and expected_output is None:
            methods_line, params_line, expected_output = _build_default_system_case(class_def)
        elif methods_line is None or params_line is None:
            return 1, "Both `methods_line` and `params_line` are required for custom testcases."

        solution_code = go_generate_system_code(class_def)
        trailer_code = go_generate_system_trailer_code(class_def)

        ret, message = prepare_go_workspace(solution_code, trailer_code, [methods_line, params_line], tmp_dir=TMP_DIR)
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

        if expected_output is not None:
            user_out_path = os.path.join(TMP_DIR, "user.out")
            with open(user_out_path, "r") as fp:
                output_lines = [line.strip() for line in fp.readlines() if line.strip()]
            if not output_lines:
                return 1, "Generated program completed but `user.out` is empty."
            if output_lines[0] != expected_output:
                return 1, f"System template output mismatch. expected={expected_output}, actual={output_lines[0]}"

        return 0, {"main_body.go": solution_code, "main_trailer.go": trailer_code}
    finally:
        shutil.rmtree(TMP_DIR, ignore_errors=True)
