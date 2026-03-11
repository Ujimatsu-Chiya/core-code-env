"""C generator logic for classic function-style problems."""

from code_gen.utils import TypeEnum, json_default_val
from code_gen.core.workspace import create_tmp_workspace, cleanup_tmp_workspace
from .common import (
    C_TYPE_SPECS,
    TIME_COST_PATH,
    CMethodDef,
    generate_c_signature,
    _c_call_args_for_param,
    _c_return_call_args,
    _c_return_aux_decl_lines,
    _c_cleanup_lines,
    prepare_c_workspace,
    compile_c_workspace,
    run_c_workspace,
    check_required_files,
)


def c_generate_solution_code(method_def: CMethodDef) -> str:
    signature = generate_c_signature(
        method_def.function_name,
        method_def.params_type,
        method_def.params_name,
        method_def.return_type,
    )
    lines = [
        f"{signature} {{",
        "    // write code here",
    ]
    if method_def.return_type == TypeEnum.NONE:
        lines.append("    return;")
    else:
        lines.append(f"    return {C_TYPE_SPECS[method_def.return_type].default};")
    lines.append("}")
    return "\n".join(lines)


def _build_param_parse_lines(method_def: CMethodDef):
    parse_lines = []
    call_args = []
    cleanup_lines = []
    for idx, (p_type, p_name) in enumerate(zip(method_def.params_type, method_def.params_name)):
        parse_lines += [
            "json_str = read_line(reader);",
            "if (json_str == NULL) {",
            "    break;" if idx == 0 else f'    fprintf(stderr, "Testcase is missing the required argument: `{p_name}`");',
            "" if idx == 0 else "    exit(1);",
            "}",
        ]
        parse_lines = [line for line in parse_lines if line != ""]

        dim = TypeEnum.get_dimension(p_type)
        if dim == 0:
            parse_lines.append(f"{C_TYPE_SPECS[p_type].lang_type} p{idx} = {C_TYPE_SPECS[p_type].des_func}(json_str);")
        elif dim == 1:
            parse_lines.append(f"size_t p{idx}_size = 0;")
            parse_lines.append(
                f"{C_TYPE_SPECS[p_type].lang_type} p{idx} = {C_TYPE_SPECS[p_type].des_func}(json_str, &p{idx}_size);"
            )
        else:
            parse_lines.append(f"size_t p{idx}_rows = 0;")
            parse_lines.append(f"size_t* p{idx}_cols = NULL;")
            parse_lines.append(
                f"{C_TYPE_SPECS[p_type].lang_type} p{idx} = {C_TYPE_SPECS[p_type].des_func}(json_str, &p{idx}_rows, &p{idx}_cols);"
            )

        call_args.extend(_c_call_args_for_param(p_type, f"p{idx}"))
        cleanup_lines.extend(_c_cleanup_lines(p_type, f"p{idx}"))

    return parse_lines, call_args, cleanup_lines


def c_generate_trailer_code(method_def: CMethodDef) -> str:
    parse_lines, call_args, arg_cleanup_lines = _build_param_parse_lines(method_def)
    ret_aux_decl = _c_return_aux_decl_lines(method_def.return_type)
    call_args_with_ret = call_args + _c_return_call_args(method_def.return_type)

    lines = [
        "",
        "void run() {",
        "    StdinWrapper* reader = create_stdin_wrapper();",
        "    StdoutWrapper* writer = create_stdout_wrapper();",
        "    char* json_str = NULL;",
        "    unsigned long long total_time = 0;",
        "    while (true) {",
        "\n".join(" " * 8 + line for line in parse_lines),
        "",
        *[" " * 8 + line for line in ret_aux_decl],
        "        unsigned long long start_stamp = __get_cpu_time();",
    ]

    if method_def.return_type == TypeEnum.NONE:
        lines += [
            f"        {method_def.function_name}({', '.join(call_args_with_ret)});",
            "        unsigned long long end_stamp = __get_cpu_time();",
            "        total_time += (end_stamp - start_stamp);",
            '        write_line(writer, "null");',
        ]
    else:
        lines += [
            f"        {C_TYPE_SPECS[method_def.return_type].lang_type} result = {method_def.function_name}({', '.join(call_args_with_ret)});",
            "        unsigned long long end_stamp = __get_cpu_time();",
            "        total_time += (end_stamp - start_stamp);",
        ]
        dim = TypeEnum.get_dimension(method_def.return_type)
        if dim == 0:
            lines.append(f"        char* result_str = {C_TYPE_SPECS[method_def.return_type].ser_func}(result);")
        elif dim == 1:
            lines.append(f"        char* result_str = {C_TYPE_SPECS[method_def.return_type].ser_func}(result, result_size);")
        else:
            lines.append(
                f"        char* result_str = {C_TYPE_SPECS[method_def.return_type].ser_func}(result, result_rows, result_cols);"
            )
        lines += [
            "        write_line(writer, result_str);",
            "        delete_string(result_str);",
            *[" " * 8 + line for line in _c_cleanup_lines(method_def.return_type, "result")],
        ]

    lines += [
        *[" " * 8 + line for line in arg_cleanup_lines],
        "    }",
        "    delete_stdin_wrapper(reader);",
        "    delete_stdout_wrapper(writer);",
        f'    FILE* fp = fopen("{TIME_COST_PATH}", "w");',
        '    fprintf(fp, "%llu", total_time / 1000000ULL);',
        "    fclose(fp);",
        "}",
        "",
        "int main() {",
        "    run();",
        "    return 0;",
        "}",
    ]

    return "\n".join(lines)


def c_test(method_def: CMethodDef):
    tmp_dir = create_tmp_workspace("code_gen_c_")
    try:
        input_lines = [json_default_val[p_type] for p_type in method_def.params_type]
        solution_code = c_generate_solution_code(method_def)
        trailer_code = c_generate_trailer_code(method_def)

        ret, message = prepare_c_workspace(solution_code, trailer_code, input_lines, tmp_dir=tmp_dir)
        if ret != 0:
            return ret, message

        ret, message = compile_c_workspace(tmp_dir=tmp_dir)
        if ret != 0:
            return ret, message

        ret, message = run_c_workspace(tmp_dir=tmp_dir)
        if ret != 0:
            return ret, message

        ret, message = check_required_files(tmp_dir=tmp_dir)
        if ret != 0:
            return ret, message

        return 0, {"main_body.c": solution_code, "main_trailer.c": trailer_code}
    finally:
        cleanup_tmp_workspace(tmp_dir)
