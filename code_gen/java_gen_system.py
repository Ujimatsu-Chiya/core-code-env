"""Java generator logic for system-design style problems."""

import json
import os
import shutil
from typing import List, Optional, Tuple

from utils import TypeEnum, json_default_val
from java_gen_common import (
    JAVA_TYPE_SPECS,
    TIME_COST_PATH,
    TMP_DIR,
    JavaClassDef,
    JavaMethodDef,
    prepare_java_workspace,
    compile_java_workspace,
    run_java_workspace,
    check_required_files,
)


def _generate_api_usage_comment(class_def: JavaClassDef) -> str:
    ctor_args = ", ".join(class_def.constructor.params_name)
    lines = [
        "/**",
        f" * Your {class_def.name} object will be instantiated and called as such:",
        f" * {class_def.name} obj = new {class_def.name}({ctor_args});",
    ]
    for idx, method in enumerate(class_def.methods, start=1):
        m_args = ", ".join(method.params_name)
        if method.return_type == TypeEnum.NONE:
            lines.append(f" * obj.{method.function_name}({m_args});")
        else:
            lines.append(
                f" * {JAVA_TYPE_SPECS[method.return_type].lang_type} result_{idx} = obj.{method.function_name}({m_args});"
            )
    lines += [" */"]
    return "\n".join(lines)


def java_generate_system_code(class_def: JavaClassDef) -> str:
    lines = [
        f"class {class_def.name}{{",
        f"    {class_def.constructor_generate()}{{",
        "        // write code here",
        "    }",
        "",
    ]
    for method_def in class_def.methods:
        lines += [
            f"    {method_def.generate()}{{",
            "        // write code here",
            (
                "        return;"
                if method_def.return_type == TypeEnum.NONE
                else f"        return {JAVA_TYPE_SPECS[method_def.return_type].default};"
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


def _java_generate_system_dispatch_block(method_defs: List[JavaMethodDef]) -> str:
    lines: List[str] = []
    for idx, method_def in enumerate(method_defs):
        branch = "if" if idx == 0 else "else if"
        lines.append(f'        {branch} (method.equals("{method_def.function_name}")) {{')
        lines.append(f"            if (paramsCur.length != {len(method_def.params_type)}) {{")
        lines.append(f'                throw new IllegalArgumentException("Method `{method_def.function_name}` argument size mismatch.");')
        lines.append("            }")

        for p_idx, p_type in enumerate(method_def.params_type):
            spec = JAVA_TYPE_SPECS[p_type]
            lines.append(f"            {spec.lang_type} p{p_idx} = JavaParseTools.{spec.des_func}(paramsCur[{p_idx}]);")

        args = ", ".join(f"p{i}" for i in range(len(method_def.params_type)))
        lines.append("            long startStamp = System.nanoTime();")
        if method_def.return_type == TypeEnum.NONE:
            lines.append(f"            obj.{method_def.function_name}({args});")
            lines.append("            long endStamp = System.nanoTime();")
            lines.append("            ctimeTotal += endStamp - startStamp;")
            lines.append('            return "null";')
        else:
            ret_spec = JAVA_TYPE_SPECS[method_def.return_type]
            lines.append(f"            {ret_spec.lang_type} ret = obj.{method_def.function_name}({args});")
            lines.append("            long endStamp = System.nanoTime();")
            lines.append("            ctimeTotal += endStamp - startStamp;")
            lines.append(f"            return JavaParseTools.{ret_spec.ser_func}(ret);")
        lines.append("        }")

    lines.append("        else {")
    lines.append('            throw new IllegalArgumentException("Input method does not exist.");')
    lines.append("        }")
    return "\n".join(lines)


def java_generate_system_trailer_code(class_def: JavaClassDef) -> str:
    ctor = class_def.constructor
    ctor_param_count = len(ctor.params_type)
    ctor_parse_lines = [
        f"            if (params[0].length != {ctor_param_count}) {{",
        '                throw new IllegalArgumentException("Constructor argument size mismatch.");',
        "            }",
    ]
    for idx, p_type in enumerate(ctor.params_type):
        spec = JAVA_TYPE_SPECS[p_type]
        ctor_parse_lines.append(f"            {spec.lang_type} ctorP{idx} = JavaParseTools.{spec.des_func}(params[0][{idx}]);")

    ctor_args = ", ".join(f"ctorP{i}" for i in range(ctor_param_count))
    dispatch_block = _java_generate_system_dispatch_block(class_def.methods)

    lines = [
        "",
        "class DriverSystemSolution {",
        "    long ctimeTotal = 0;",
        "",
        f"    String dispatch(String method, String[] paramsCur, {class_def.name} obj) {{",
        dispatch_block,
        "    }",
        "",
        "    String solve(String[] methods, String[][] params) {",
        "        if (methods.length == 0 || params.length == 0 || methods.length != params.length) {",
        '            throw new IllegalArgumentException("Input methods size does not equal to params size or equals to 0.");',
        "        }",
        f'        if (!methods[0].equals("{class_def.name}")) {{',
        '            throw new IllegalArgumentException("First method is not constructor.");',
        "        }",
        "\n".join(ctor_parse_lines),
        "        long ctorStartStamp = System.nanoTime();",
        f"        {class_def.name} obj = new {class_def.name}({ctor_args});",
        "        long ctorEndStamp = System.nanoTime();",
        "        ctimeTotal += ctorEndStamp - ctorStartStamp;",
        "",
        "        List<String> outputs = new ArrayList<>();",
        '        outputs.add("null");',
        "        for (int i = 1; i < methods.length; i++) {",
        "            outputs.add(dispatch(methods[i], params[i], obj));",
        "        }",
        '        return "[" + String.join(",", outputs) + "]";',
        "    }",
        "}",
        "",
        "public class Main {",
        "    public static void run() throws IOException {",
        "        StdinWrapper reader = new StdinWrapper();",
        "        StdoutWrapper writer = new StdoutWrapper();",
        "        DriverSystemSolution driver = new DriverSystemSolution();",
        "        while (true) {",
        "            String lineMethods = reader.readLine();",
        "            if (lineMethods == null) {",
        "                break;",
        "            }",
        "            String lineParams = reader.readLine();",
        "            if (lineParams == null) {",
        '                throw new IllegalArgumentException("Testcase is missing the required argument: `params`");',
        "            }",
        "            String[] methods = JavaParseTools.desStringList(lineMethods);",
        "            String[][] params = JavaParseTools.desJsonValueListList(lineParams);",
        "            writer.writeLine(driver.solve(methods, params));",
        "        }",
        f'        try (BufferedWriter fp = new BufferedWriter(new FileWriter("{TIME_COST_PATH}"))) {{',
        '            fp.write(String.format("%d", driver.ctimeTotal / 1000000));',
        "        }",
        "    }",
        "",
        "    public static void main(String[] args) {",
        "        try {",
        "            run();",
        "        } catch (Exception e) {",
        "            e.printStackTrace();",
        "            System.exit(1);",
        "        }",
        "    }",
        "}",
    ]
    return "\n".join(lines)


def _build_default_system_case(class_def: JavaClassDef) -> Tuple[str, str, str]:
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


def java_system_test(
    class_def: JavaClassDef,
    methods_line: Optional[str] = None,
    params_line: Optional[str] = None,
    expected_output: Optional[str] = None,
):
    try:
        if methods_line is None and params_line is None and expected_output is None:
            methods_line, params_line, expected_output = _build_default_system_case(class_def)
        elif methods_line is None or params_line is None:
            return 1, "Both `methods_line` and `params_line` are required for custom testcases."

        solution_code = java_generate_system_code(class_def)
        trailer_code = java_generate_system_trailer_code(class_def)

        ret, message = prepare_java_workspace(solution_code, trailer_code, [methods_line, params_line], tmp_dir=TMP_DIR)
        if ret != 0:
            return ret, message

        ret, message = compile_java_workspace(tmp_dir=TMP_DIR)
        if ret != 0:
            return ret, message

        ret, message = run_java_workspace(tmp_dir=TMP_DIR)
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

        return 0, {"main_body.java": solution_code, "main_trailer.java": trailer_code}
    finally:
        shutil.rmtree(TMP_DIR, ignore_errors=True)
