"""C generator logic for system-design style problems."""

import json
import os
import shutil
from typing import List, Optional, Tuple

from utils import TypeEnum, json_default_val
from c_gen_common import (
    C_TYPE_SPECS,
    TIME_COST_PATH,
    TMP_DIR,
    CClassDef,
    CMethodDef,
    build_c_method_signature_for_system,
    build_c_constructor_signature_for_system,
    build_c_destructor_signature_for_system,
    _c_call_args_for_param,
    _c_return_call_args,
    _c_return_aux_decl_lines,
    _c_cleanup_lines,
    prepare_c_workspace,
    compile_c_workspace,
    run_c_workspace,
    check_required_files,
)


def _generate_api_usage_comment(class_def: CClassDef) -> str:
    ctor_args = ", ".join(class_def.constructor.params_name)
    lines = [
        "/**",
        f" * Your {class_def.name} struct will be instantiated and called as such:",
        f" * {class_def.name}* obj = {class_def.constructor_c_name()}({ctor_args});",
    ]
    for idx, method in enumerate(class_def.methods, start=1):
        m_args = ", ".join(method.params_name)
        if method.return_type == TypeEnum.NONE:
            lines.append(f" * {class_def.method_c_name(method)}(obj{', ' if m_args else ''}{m_args});")
        else:
            lines.append(
                f" * {C_TYPE_SPECS[method.return_type].lang_type} result_{idx} = {class_def.method_c_name(method)}(obj{', ' if m_args else ''}{m_args});"
            )
    lines += [
        f" * {class_def.destructor_c_name()}(obj);",
        " */",
    ]
    return "\n".join(lines)


def c_generate_system_code(class_def: CClassDef) -> str:
    lines = [
        f"typedef struct {class_def.name} {{",
        "    // write code here",
        f"}} {class_def.name};",
        "",
        "/** initialize your data structure here. */",
        "",
        f"{build_c_constructor_signature_for_system(class_def)} {{",
        "    // write code here",
        "    return NULL;",
        "}",
        "",
    ]

    for method in class_def.methods:
        lines += [
            f"{build_c_method_signature_for_system(class_def, method)} {{",
            "    // write code here",
            "    return;" if method.return_type == TypeEnum.NONE else f"    return {C_TYPE_SPECS[method.return_type].default};",
            "}",
            "",
        ]

    lines += [
        f"{build_c_destructor_signature_for_system(class_def)} {{",
        "    // write code here",
        "}",
        "",
        _generate_api_usage_comment(class_def),
    ]
    return "\n".join(lines)


def _build_dispatch_branch(class_def: CClassDef, method_def: CMethodDef, is_first: bool) -> List[str]:
    branch = "if" if is_first else "else if"
    lines = [
        f'    {branch} (strcmp(method, "{method_def.function_name}") == 0) {{',
        f"        if (params_cur_size != {len(method_def.params_type)}) {{",
        f'            fprintf(stderr, "Method `{method_def.function_name}` argument size mismatch.");',
        "            exit(1);",
        "        }",
    ]

    call_args = ["obj"]
    for idx, p_type in enumerate(method_def.params_type):
        dim = TypeEnum.get_dimension(p_type)
        if dim == 0:
            lines.append(f"        {C_TYPE_SPECS[p_type].lang_type} p{idx} = {C_TYPE_SPECS[p_type].des_func}(params_cur[{idx}]);")
        elif dim == 1:
            lines.append(f"        size_t p{idx}_size = 0;")
            lines.append(
                f"        {C_TYPE_SPECS[p_type].lang_type} p{idx} = {C_TYPE_SPECS[p_type].des_func}(params_cur[{idx}], &p{idx}_size);"
            )
        else:
            lines.append(f"        size_t p{idx}_rows = 0;")
            lines.append(f"        size_t* p{idx}_cols = NULL;")
            lines.append(
                f"        {C_TYPE_SPECS[p_type].lang_type} p{idx} = {C_TYPE_SPECS[p_type].des_func}(params_cur[{idx}], &p{idx}_rows, &p{idx}_cols);"
            )
        call_args.extend(_c_call_args_for_param(p_type, f"p{idx}"))

    lines.extend("        " + s for s in _c_return_aux_decl_lines(method_def.return_type))
    call_args.extend(_c_return_call_args(method_def.return_type))

    lines += [
        "        unsigned long long start_stamp = __get_cpu_time();",
    ]

    call_expr = f"{class_def.method_c_name(method_def)}({', '.join(call_args)})"
    if method_def.return_type == TypeEnum.NONE:
        lines += [
            f"        {call_expr};",
            "        unsigned long long end_stamp = __get_cpu_time();",
            "        driver->ctime_total += (end_stamp - start_stamp);",
        ]
        lines.extend("        " + s for i, t in enumerate(method_def.params_type) for s in _c_cleanup_lines(t, f"p{i}"))
        lines += [
            "        *is_null_output = true;",
            "        return NULL;",
            "    }",
        ]
        return lines

    lines += [
        f"        {C_TYPE_SPECS[method_def.return_type].lang_type} result = {call_expr};",
        "        unsigned long long end_stamp = __get_cpu_time();",
        "        driver->ctime_total += (end_stamp - start_stamp);",
    ]

    dim = TypeEnum.get_dimension(method_def.return_type)
    if dim == 0:
        lines.append(f"        char* result_json = {C_TYPE_SPECS[method_def.return_type].ser_func}(result);")
    elif dim == 1:
        lines.append(f"        char* result_json = {C_TYPE_SPECS[method_def.return_type].ser_func}(result, result_size);")
    else:
        lines.append(
            f"        char* result_json = {C_TYPE_SPECS[method_def.return_type].ser_func}(result, result_rows, result_cols);"
        )

    lines.extend("        " + s for s in _c_cleanup_lines(method_def.return_type, "result"))
    lines.extend("        " + s for i, t in enumerate(method_def.params_type) for s in _c_cleanup_lines(t, f"p{i}"))
    lines += [
        "        *is_null_output = false;",
        "        return result_json;",
        "    }",
    ]
    return lines


def c_generate_system_trailer_code(class_def: CClassDef) -> str:
    ctor_parse_lines: List[str] = [
        f"    if (params_cols[0] != {len(class_def.constructor.params_type)}) {{",
        '        fprintf(stderr, "Constructor argument size mismatch.");',
        "        exit(1);",
        "    }",
    ]
    ctor_call_args: List[str] = []
    ctor_cleanup_lines: List[str] = []
    for idx, p_type in enumerate(class_def.constructor.params_type):
        dim = TypeEnum.get_dimension(p_type)
        if dim == 0:
            ctor_parse_lines.append(
                f"    {C_TYPE_SPECS[p_type].lang_type} ctor_p{idx} = {C_TYPE_SPECS[p_type].des_func}(params[0][{idx}]);"
            )
        elif dim == 1:
            ctor_parse_lines.append(f"    size_t ctor_p{idx}_size = 0;")
            ctor_parse_lines.append(
                f"    {C_TYPE_SPECS[p_type].lang_type} ctor_p{idx} = {C_TYPE_SPECS[p_type].des_func}(params[0][{idx}], &ctor_p{idx}_size);"
            )
        else:
            ctor_parse_lines.append(f"    size_t ctor_p{idx}_rows = 0;")
            ctor_parse_lines.append(f"    size_t* ctor_p{idx}_cols = NULL;")
            ctor_parse_lines.append(
                f"    {C_TYPE_SPECS[p_type].lang_type} ctor_p{idx} = {C_TYPE_SPECS[p_type].des_func}(params[0][{idx}], &ctor_p{idx}_rows, &ctor_p{idx}_cols);"
            )
        ctor_call_args.extend(_c_call_args_for_param(p_type, f"ctor_p{idx}"))
        ctor_cleanup_lines.extend(_c_cleanup_lines(p_type, f"ctor_p{idx}"))

    dispatch_lines: List[str] = []
    for idx, method in enumerate(class_def.methods):
        dispatch_lines.extend(_build_dispatch_branch(class_def, method, idx == 0))

    lines = [
        "",
        "typedef struct {",
        "    unsigned long long ctime_total;",
        "} DriverSystemSolution;",
        "",
        "static char* __join_json__(char** parts, size_t part_count) {",
        "    size_t total_len = 2;",
        "    if (part_count > 1) {",
        "        total_len += (part_count - 1);",
        "    }",
        "    for (size_t i = 0; i < part_count; ++i) {",
        "        total_len += strlen(parts[i]);",
        "    }",
        "    char* out_json = (char*)malloc(total_len + 1);",
        "    if (out_json == NULL) {",
        '        fprintf(stderr, "Memory allocation failed.");',
        "        exit(1);",
        "    }",
        "    char* p = out_json;",
        "    *p++ = '[';",
        "    for (size_t i = 0; i < part_count; ++i) {",
        "        size_t cur_len = strlen(parts[i]);",
        "        memcpy(p, parts[i], cur_len);",
        "        p += cur_len;",
        "        if (i + 1 < part_count) {",
        "            *p++ = ',';",
        "        }",
        "    }",
        "    *p++ = ']';",
        "    *p = '\\0';",
        "    return out_json;",
        "}",
        "",
        "static char* __dispatch__(DriverSystemSolution* driver, const char* method, char** params_cur, size_t params_cur_size, "
        + f"{class_def.name}* obj, bool* is_null_output) {{",
        *dispatch_lines,
        "    else {",
        '        fprintf(stderr, "Input method does not exist.");',
        "        exit(1);",
        "    }",
        "    return NULL;",
        "}",
        "",
        "static char* __solve__(DriverSystemSolution* driver, char** methods, size_t methods_size, char*** params, size_t params_rows, size_t* params_cols) {",
        "    if (methods_size == 0 || params_rows == 0 || methods_size != params_rows) {",
        '        fprintf(stderr, "Input methods size does not equal to params size or equals to 0.");',
        "        exit(1);",
        "    }",
        f'    if (strcmp(methods[0], "{class_def.name}") != 0) {{',
        '        fprintf(stderr, "First method is not constructor.");',
        "        exit(1);",
        "    }",
        *ctor_parse_lines,
        "    unsigned long long ctor_start_stamp = __get_cpu_time();",
        f"    {class_def.name}* obj = {class_def.constructor_c_name()}({', '.join(ctor_call_args)});",
        "    unsigned long long ctor_end_stamp = __get_cpu_time();",
        "    driver->ctime_total += (ctor_end_stamp - ctor_start_stamp);",
        *ctor_cleanup_lines,
        "    char** outputs = (char**)malloc(sizeof(char*) * methods_size);",
        "    bool* outputs_owned = (bool*)calloc(methods_size, sizeof(bool));",
        "    if (outputs == NULL || outputs_owned == NULL) {",
        '        fprintf(stderr, "Memory allocation failed.");',
        "        exit(1);",
        "    }",
        '    outputs[0] = "null";',
        "    for (size_t i = 1; i < methods_size; ++i) {",
        "        bool is_null_output = false;",
        "        char* result_json = __dispatch__(driver, methods[i], params[i], params_cols[i], obj, &is_null_output);",
        "        if (is_null_output) {",
        '            outputs[i] = "null";',
        "        } else {",
        "            outputs[i] = result_json;",
        "            outputs_owned[i] = true;",
        "        }",
        "    }",
        "    char* out_json = __join_json__(outputs, methods_size);",
        "    for (size_t i = 0; i < methods_size; ++i) {",
        "        if (outputs_owned[i]) {",
        "            delete_string(outputs[i]);",
        "        }",
        "    }",
        "    free(outputs);",
        "    free(outputs_owned);",
        "    if (obj != NULL) {",
        f"        {class_def.destructor_c_name()}(obj);",
        "    }",
        "    return out_json;",
        "}",
        "",
        "void run() {",
        "    StdinWrapper* reader = create_stdin_wrapper();",
        "    StdoutWrapper* writer = create_stdout_wrapper();",
        "    DriverSystemSolution driver = {0};",
        "    while (true) {",
        "        char* line_methods = read_line(reader);",
        "        if (line_methods == NULL) {",
        "            break;",
        "        }",
        "        size_t methods_size = 0;",
        "        char** methods = des_string_list(line_methods, &methods_size);",
        "        char* line_params = read_line(reader);",
        "        if (line_params == NULL) {",
        '            fprintf(stderr, "Testcase is missing the required argument: `params`");',
        "            exit(1);",
        "        }",
        "        size_t params_rows = 0;",
        "        size_t* params_cols = NULL;",
        "        char*** params = des_json_value_list_list(line_params, &params_rows, &params_cols);",
        "        char* output_json = __solve__(&driver, methods, methods_size, params, params_rows, params_cols);",
        "        write_line(writer, output_json);",
        "        free(output_json);",
        "        delete_string_list(methods, methods_size);",
        "        delete_json_value_list_list(params, params_rows, params_cols);",
        "    }",
        "    delete_stdin_wrapper(reader);",
        "    delete_stdout_wrapper(writer);",
        f'    FILE* fp = fopen("{TIME_COST_PATH}", "w");',
        '    fprintf(fp, "%llu", driver.ctime_total / 1000000ULL);',
        "    fclose(fp);",
        "}",
        "",
        "int main() {",
        "    run();",
        "    return 0;",
        "}",
    ]
    return "\n".join(lines)


def _build_default_system_case(class_def: CClassDef) -> Tuple[str, str, str]:
    methods = [class_def.name] + [method.function_name for method in class_def.methods]

    params = []
    ctor_values = [json.loads(json_default_val[p_type]) for p_type in class_def.constructor.params_type]
    params.append(ctor_values)
    for method in class_def.methods:
        method_values = [json.loads(json_default_val[p_type]) for p_type in method.params_type]
        params.append(method_values)

    def _default_output_value(p_type: TypeEnum):
        if p_type == TypeEnum.NONE:
            return None
        if p_type in [TypeEnum.BOOL]:
            return False
        if p_type in [TypeEnum.INT, TypeEnum.LONG]:
            return 0
        if p_type == TypeEnum.DOUBLE:
            return 0.0
        if p_type == TypeEnum.STRING:
            return ""
        if p_type in [
            TypeEnum.INT_LIST,
            TypeEnum.INT_LIST_LIST,
            TypeEnum.DOUBLE_LIST,
            TypeEnum.STRING_LIST,
            TypeEnum.BOOL_LIST,
            TypeEnum.LONG_LIST,
            TypeEnum.TREENODE,
            TypeEnum.LISTNODE,
        ]:
            return []
        raise ValueError(f"Unsupported type: {p_type}")

    outputs: List[object] = [None]
    for method in class_def.methods:
        outputs.append(_default_output_value(method.return_type))

    methods_line = json.dumps(methods, separators=(",", ":"))
    params_line = json.dumps(params, separators=(",", ":"))
    expected_output = json.dumps(outputs, separators=(",", ":"))
    return methods_line, params_line, expected_output


def c_system_test(
    class_def: CClassDef,
    methods_line: Optional[str] = None,
    params_line: Optional[str] = None,
    expected_output: Optional[str] = None,
):
    try:
        if methods_line is None and params_line is None and expected_output is None:
            methods_line, params_line, expected_output = _build_default_system_case(class_def)
        elif methods_line is None or params_line is None:
            return 1, "Both `methods_line` and `params_line` are required for custom testcases."

        solution_code = c_generate_system_code(class_def)
        trailer_code = c_generate_system_trailer_code(class_def)

        ret, message = prepare_c_workspace(solution_code, trailer_code, [methods_line, params_line], tmp_dir=TMP_DIR)
        if ret != 0:
            return ret, message

        ret, message = compile_c_workspace(tmp_dir=TMP_DIR)
        if ret != 0:
            return ret, message

        ret, message = run_c_workspace(tmp_dir=TMP_DIR)
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

        return 0, {"main_body.c": solution_code, "main_trailer.c": trailer_code}
    finally:
        shutil.rmtree(TMP_DIR, ignore_errors=True)
