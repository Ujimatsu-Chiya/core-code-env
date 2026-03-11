"""C++ generator logic for classic function-style problems."""

from code_gen.utils import TypeEnum, json_default_val
from code_gen.core.workspace import create_tmp_workspace, cleanup_tmp_workspace
from .common import (
    CPP_TYPE_SPECS,
    TIME_COST_PATH,
    CppMethodDef,
    prepare_cpp_workspace,
    compile_cpp_workspace,
    run_cpp_workspace,
    check_required_files,
)


def _cpp_driver_param_type(type_enum):
    lang_type = CPP_TYPE_SPECS[type_enum].lang_type
    if lang_type.startswith("vector<") or lang_type == "string":
        return f"{lang_type}&"
    return lang_type


def _cpp_generate_driver_code(method_def: CppMethodDef):
    helper_params = ", ".join(
        f"{_cpp_driver_param_type(p_type)} param_{idx + 1}"
        for idx, p_type in enumerate(method_def.params_type)
    )
    helper_args = ", ".join(f"param_{idx + 1}" for idx in range(len(method_def.params_type)))
    return_type = CPP_TYPE_SPECS[method_def.return_type].lang_type
    if method_def.return_type == TypeEnum.NONE:
        helper_body = [
            f"        Solution().{method_def.function_name}({helper_args});",
        ]
    else:
        helper_body = [
            f"        {return_type} ret = Solution().{method_def.function_name}({helper_args});",
            "        return ret;",
        ]
    return [
        "class __DriverSolution__ {",
        "public:",
        f"    {return_type} __helper__({helper_params}) {{",
        *helper_body,
        "    }",
        "};",
    ]


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
    driver_code = _cpp_generate_driver_code(method_def)
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
        *driver_code,
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
        f'        {CPP_TYPE_SPECS[method_def.return_type].lang_type} result = __DriverSolution__().__helper__({", ".join(f"p{x}" for x in range(params_num))});',
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
    tmp_dir = create_tmp_workspace("code_gen_cpp_")
    try:
        input_lines = [json_default_val[p_type] for p_type in method_def.params_type]
        solution_code = cpp_generate_solution_code(method_def)
        trailer_code = cpp_generate_trailer_code(method_def)

        ret, message = prepare_cpp_workspace(solution_code, trailer_code, input_lines, tmp_dir=tmp_dir)
        if ret != 0:
            return ret, message

        ret, message = compile_cpp_workspace(tmp_dir=tmp_dir)
        if ret != 0:
            return ret, message

        ret, message = run_cpp_workspace(tmp_dir=tmp_dir)
        if ret != 0:
            return ret, message

        ret, message = check_required_files(tmp_dir=tmp_dir)
        if ret != 0:
            return ret, message

        return 0, {"main_body.cpp": solution_code, "main_trailer.cpp": trailer_code}
    finally:
        cleanup_tmp_workspace(tmp_dir)
