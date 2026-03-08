"""C++ generator logic for classic function-style problems."""

import shutil

from utils import json_default_val
from cpp_gen_common import (
    CPP_TYPE_SPECS,
    TIME_COST_PATH,
    TMP_DIR,
    CppMethodDef,
    prepare_cpp_workspace,
    compile_cpp_workspace,
    run_cpp_workspace,
    check_required_files,
)


def cpp_generate_solution_code(method_def: CppMethodDef):
    lines = [
        "class Solution{",
        "public:",
        f"    {method_def.generate()}{{",
        "        // write code here",
        f"        return {CPP_TYPE_SPECS[method_def.return_type].default};",
        "    }",
        "};",
    ]
    return "\n".join(lines)


def cpp_generate_trailer_code(method_def: CppMethodDef):
    params_num = len(method_def.params_name)
    lines_pre = []
    for i, (p_type, p_name) in enumerate(zip(method_def.params_type, method_def.params_name)):
        lines_pre += [
            "json_str = reader.read_line();",
            "if(json_str.empty()){",
            "    break;" if i == 0 else f'    throw std::invalid_argument("Testcase is missing the required argument: `{p_name}`");',
            "}",
            f"{CPP_TYPE_SPECS[p_type].lang_type} p{i} = {CPP_TYPE_SPECS[p_type].des_func}(json_str);",
        ]
    lines = [
        "",
        "void run() {",
        "    StdinWrapper reader;",
        "    StdoutWrapper writer;",
        "    string json_str;",
        "    clock_t total_time = 0;",
        "    while (true) {",
        "",
        "\n".join([" " * 8 + s for s in lines_pre]),
        "",
        "        unsigned long long start_stamp = __get_cpu_time();",
        f'        {CPP_TYPE_SPECS[method_def.return_type].lang_type} result = Solution().{method_def.function_name}({", ".join(f"p{x}" for x in range(params_num))});',
        "        unsigned long long end_stamp = __get_cpu_time();",
        "        total_time += (end_stamp - start_stamp);",
        f"        string result_str = {CPP_TYPE_SPECS[method_def.return_type].ser_func}(result);",
        "        writer.write_line(result_str);",
        "    }",
        "",
        f'    std::ofstream fp("{TIME_COST_PATH}");',
        "    fp << total_time / 100000UL;",
        "}",
        "",
        "int main() {",
        "    try {",
        "        run();",
        "    } catch (const std::exception& e) {",
        "        std::cerr << e.what() << std::endl;",
        "        return 1;",
        "    }",
        "    return 0;",
        "}",
    ]

    return "\n".join(lines)


def cpp_test(method_def: CppMethodDef):
    try:
        input_lines = [json_default_val[p_type] for p_type in method_def.params_type]
        solution_code = cpp_generate_solution_code(method_def)
        trailer_code = cpp_generate_trailer_code(method_def)

        ret, message = prepare_cpp_workspace(solution_code, trailer_code, input_lines, tmp_dir=TMP_DIR)
        if ret != 0:
            return ret, message

        ret, message = compile_cpp_workspace(tmp_dir=TMP_DIR)
        if ret != 0:
            return ret, message

        ret, message = run_cpp_workspace(tmp_dir=TMP_DIR)
        if ret != 0:
            return ret, message

        ret, message = check_required_files(tmp_dir=TMP_DIR)
        if ret != 0:
            return ret, message

        return 0, {"main_body.cpp": solution_code, "main_trailer.cpp": trailer_code}
    finally:
        shutil.rmtree(TMP_DIR, ignore_errors=True)

