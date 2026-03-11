"""Java generator logic for classic function-style problems."""

from code_gen.utils import TypeEnum, json_default_val
from code_gen.core.workspace import create_tmp_workspace, cleanup_tmp_workspace
from .common import (
    JAVA_TYPE_SPECS,
    TIME_COST_PATH,
    JavaMethodDef,
    prepare_java_workspace,
    compile_java_workspace,
    run_java_workspace,
    check_required_files,
)


def _java_generate_driver_code(method_def: JavaMethodDef) -> str:
    helper_params = ", ".join(
        f"{JAVA_TYPE_SPECS[p_type].lang_type} param_{idx + 1}"
        for idx, p_type in enumerate(method_def.params_type)
    )
    helper_args = ", ".join(f"param_{idx + 1}" for idx in range(len(method_def.params_type)))
    return_type = JAVA_TYPE_SPECS[method_def.return_type].lang_type

    if method_def.return_type == TypeEnum.NONE:
        helper_body = [
            f"        new Solution().{method_def.function_name}({helper_args});",
            "        return;",
        ]
    else:
        helper_body = [
            f"        {return_type} ret = new Solution().{method_def.function_name}({helper_args});",
            "        return ret;",
        ]

    lines = [
        "class __DriverSolution__ {",
        f"    public {return_type} __helper__({helper_params}) {{",
        *helper_body,
        "    }",
        "}",
    ]
    return "\n".join(lines)


def java_generate_solution_code(method_def: JavaMethodDef) -> str:
    return_line = (
        "        return;"
        if method_def.return_type == TypeEnum.NONE
        else f"        return {JAVA_TYPE_SPECS[method_def.return_type].default};"
    )
    lines = [
        "class Solution{",
        f"    {method_def.generate()}{{",
        "        // write code here",
        return_line,
        "    }",
        "}",
    ]
    return "\n".join(lines)


def java_generate_trailer_code(method_def: JavaMethodDef) -> str:
    params_num = len(method_def.params_name)
    driver_code = _java_generate_driver_code(method_def)
    lines_pre = []
    for i, (p_type, p_name) in enumerate(zip(method_def.params_type, method_def.params_name)):
        lines_pre += [
            "jsonStr = reader.readLine();",
            "if (jsonStr == null) {",
            "    break;" if i == 0 else f'    throw new IllegalArgumentException("Testcase is missing the required argument: `{p_name}`");',
            "}",
            f"{JAVA_TYPE_SPECS[p_type].lang_type} p{i} = JavaParseTools.{JAVA_TYPE_SPECS[p_type].des_func}(jsonStr);",
        ]

    args = ", ".join(f"p{x}" for x in range(params_num))
    if method_def.return_type == TypeEnum.NONE:
        invoke_lines = [f"            driver.__helper__({args});"]
        output_lines = ['            writer.writeLine("null");']
    else:
        invoke_lines = [
            f"            {JAVA_TYPE_SPECS[method_def.return_type].lang_type} result = driver.__helper__({args});"
        ]
        output_lines = [f"            writer.writeLine(JavaParseTools.{JAVA_TYPE_SPECS[method_def.return_type].ser_func}(result));"]

    lines = [
        "",
        driver_code,
        "",
        "public class Main {",
        "    public static void run() throws IOException {",
        "        StdinWrapper reader = new StdinWrapper();",
        "        StdoutWrapper writer = new StdoutWrapper();",
        "        __DriverSolution__ driver = new __DriverSolution__();",
        "        long totalTime = 0;",
        "        String jsonStr;",
        "",
        "        while (true) {",
        "\n".join([" " * 12 + s for s in lines_pre]),
        "",
        "            long startStamp = System.nanoTime();",
        *invoke_lines,
        "            long endStamp = System.nanoTime();",
        "            totalTime += endStamp - startStamp;",
        *output_lines,
        "        }",
        "",
        f'        try (BufferedWriter fp = new BufferedWriter(new FileWriter("{TIME_COST_PATH}"))) {{',
        '            fp.write(String.format("%d", totalTime / 1000000));',
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


def java_test(method_def: JavaMethodDef):
    tmp_dir = create_tmp_workspace("code_gen_java_")
    try:
        input_lines = [json_default_val[p_type] for p_type in method_def.params_type]
        solution_code = java_generate_solution_code(method_def)
        trailer_code = java_generate_trailer_code(method_def)

        ret, message = prepare_java_workspace(solution_code, trailer_code, input_lines, tmp_dir=tmp_dir)
        if ret != 0:
            return ret, message

        ret, message = compile_java_workspace(tmp_dir=tmp_dir)
        if ret != 0:
            return ret, message

        ret, message = run_java_workspace(tmp_dir=tmp_dir)
        if ret != 0:
            return ret, message

        ret, message = check_required_files(tmp_dir=tmp_dir)
        if ret != 0:
            return ret, message

        return 0, {"main_body.java": solution_code, "main_trailer.java": trailer_code}
    finally:
        cleanup_tmp_workspace(tmp_dir)
