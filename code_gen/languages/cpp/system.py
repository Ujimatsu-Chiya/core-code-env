"""C++ generator logic for system-design style problems."""

from typing import List, Optional, Tuple

from code_gen.utils import TypeEnum
from code_gen.core.workspace import create_tmp_workspace, cleanup_tmp_workspace
from code_gen.core.system_test_utils import (
    default_output_from_json_default,
    resolve_system_case_inputs,
    verify_expected_user_output,
)
from .common import (
    CPP_TYPE_SPECS,
    TIME_COST_PATH,
    CppClassDef,
    CppMethodDef,
    prepare_cpp_workspace,
    compile_cpp_workspace,
    run_cpp_workspace,
    check_required_files,
)


def _generate_api_usage_comment(class_def: CppClassDef) -> str:
    ctor_args = ", ".join(class_def.constructor.params_name)
    lines = [
        "/**",
        f" * Your {class_def.name} object will be instantiated and called as such:",
        f" * {class_def.name}* obj = new {class_def.name}({ctor_args});",
    ]
    for idx, method in enumerate(class_def.methods, start=1):
        m_args = ", ".join(method.params_name)
        if method.return_type == TypeEnum.NONE:
            lines.append(f" * obj->{method.function_name}({m_args});")
        else:
            lines.append(
                f" * {CPP_TYPE_SPECS[method.return_type].lang_type} result_{idx} = obj->{method.function_name}({m_args});"
            )
    lines += [
        " * delete obj;",
        " */",
    ]
    return "\n".join(lines)


def cpp_generate_system_code(class_def: CppClassDef) -> str:
    lines = [
        f"class {class_def.name}{{",
        "public:",
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
                else f"        return {CPP_TYPE_SPECS[method_def.return_type].default};"
            ),
            "    }",
            "",
        ]
    lines += [
        "};",
        "",
        _generate_api_usage_comment(class_def),
    ]
    return "\n".join(lines)


def _cpp_generate_system_dispatch_block(method_defs: List[CppMethodDef], class_name: str) -> str:
    del class_name
    lines: List[str] = []
    for idx, method_def in enumerate(method_defs):
        branch = "if" if idx == 0 else "else if"
        lines.append(f'        {branch} (method == "{method_def.function_name}") {{')
        lines.append(f"            if (params_cur.size() != {len(method_def.params_type)}) {{")
        lines.append(f'                throw std::invalid_argument("Method `{method_def.function_name}` argument size mismatch.");')
        lines.append("            }")

        for p_idx, p_type in enumerate(method_def.params_type):
            spec = CPP_TYPE_SPECS[p_type]
            lines.append(f"            {spec.lang_type} p{p_idx} = {spec.des_func}(params_cur[{p_idx}]);")

        args = ", ".join(f"p{i}" for i in range(len(method_def.params_type)))
        lines.append("            unsigned long long start_stamp = __get_cpu_time();")

        if method_def.return_type == TypeEnum.NONE:
            lines.append(f"            obj->{method_def.function_name}({args});")
            lines.append("            unsigned long long end_stamp = __get_cpu_time();")
            lines.append("            ctime_total += (end_stamp - start_stamp);")
            lines.append('            return "null";')
        else:
            ret_spec = CPP_TYPE_SPECS[method_def.return_type]
            lines.append(f"            {ret_spec.lang_type} ret = obj->{method_def.function_name}({args});")
            lines.append("            unsigned long long end_stamp = __get_cpu_time();")
            lines.append("            ctime_total += (end_stamp - start_stamp);")
            lines.append(f"            return {ret_spec.ser_func}(ret);")

        lines.append("        }")

    lines.append("        else {")
    lines.append('            throw std::invalid_argument("Input method does not exist.");')
    lines.append("        }")
    return "\n".join(lines)


def cpp_generate_system_trailer_code(class_def: CppClassDef) -> str:
    ctor = class_def.constructor
    ctor_param_count = len(ctor.params_type)
    ctor_parse_lines = [
        f"        if (params[0].size() != {ctor_param_count}) {{",
        '            throw std::invalid_argument("Constructor argument size mismatch.");',
        "        }",
    ]
    for idx, p_type in enumerate(ctor.params_type):
        spec = CPP_TYPE_SPECS[p_type]
        ctor_parse_lines.append(f"        {spec.lang_type} ctor_p{idx} = {spec.des_func}(params[0][{idx}]);")

    ctor_args = ", ".join(f"ctor_p{i}" for i in range(ctor_param_count))
    dispatch_block = _cpp_generate_system_dispatch_block(class_def.methods, class_def.name)

    lines = [
        "",
        "class DriverSystemSolution {",
        "public:",
        "    unsigned long long ctime_total = 0;",
        "",
        "    static string join_json(const vector<string>& elements) {",
        "        if (elements.empty()) {",
        '            return "";',
        "        }",
        "        string result = elements[0];",
        "        for (size_t i = 1; i < elements.size(); ++i) {",
        '            result += ",";',
        "            result += elements[i];",
        "        }",
        "        return result;",
        "    }",
        "",
        f"    string dispatch(const string& method, const vector<string>& params_cur, {class_def.name}* obj) {{",
        dispatch_block,
        "    }",
        "",
        "    string solve(const vector<string>& methods, const vector<vector<string>>& params) {",
        "        if (methods.empty() || params.empty() || methods.size() != params.size()) {",
        '            throw std::invalid_argument("Input methods size does not equal to params size or equals to 0.");',
        "        }",
        f'        if (methods[0] != "{class_def.name}") {{',
        '            throw std::invalid_argument("First method is not constructor.");',
        "        }",
        "\n".join(ctor_parse_lines),
        "        unsigned long long ctor_start_stamp = __get_cpu_time();",
        f"        std::unique_ptr<{class_def.name}> obj(new {class_def.name}({ctor_args}));",
        "        unsigned long long ctor_end_stamp = __get_cpu_time();",
        "        ctime_total += (ctor_end_stamp - ctor_start_stamp);",
        "",
        "        vector<string> outputs;",
        "        outputs.reserve(methods.size());",
        '        outputs.push_back("null");',
        "        for (size_t i = 1; i < methods.size(); ++i) {",
        "            outputs.push_back(dispatch(methods[i], params[i], obj.get()));",
        "        }",
        '        return "[" + join_json(outputs) + "]";',
        "    }",
        "};",
        "",
        "void run() {",
        "    StdinWrapper reader;",
        "    StdoutWrapper writer;",
        "    DriverSystemSolution driver;",
        "    while (true) {",
        "        string line_methods = reader.read_line();",
        "        if (line_methods.empty()) {",
        "            break;",
        "        }",
        "        string line_params = reader.read_line();",
        "        if (line_params.empty()) {",
        '            throw std::invalid_argument("Testcase is missing the required argument: `params`");',
        "        }",
        "        vector<string> methods = des_string_list(line_methods);",
        "        vector<vector<string>> params = des_json_value_list_list(line_params);",
        "        writer.write_line(driver.solve(methods, params));",
        "    }",
        f'    std::ofstream fp("{TIME_COST_PATH}");',
        "    fp << driver.ctime_total / 100000UL;",
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


def cpp_system_test(
    class_def: CppClassDef,
    methods_line: Optional[str] = None,
    params_line: Optional[str] = None,
    expected_output: Optional[str] = None,
):
    tmp_dir = create_tmp_workspace("code_gen_cpp_")
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

        solution_code = cpp_generate_system_code(class_def)
        trailer_code = cpp_generate_system_trailer_code(class_def)

        ret, message = prepare_cpp_workspace(
            solution_code,
            trailer_code,
            [methods_line, params_line],
            tmp_dir=tmp_dir,
        )
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

        error = verify_expected_user_output(tmp_dir, expected_output)
        if error is not None:
            return 1, error

        return 0, {"main_body.cpp": solution_code, "main_trailer.cpp": trailer_code}
    finally:
        cleanup_tmp_workspace(tmp_dir)
