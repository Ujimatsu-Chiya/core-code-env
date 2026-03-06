"""C++ code generator for function-style and system-design style templates."""

import os
import shutil
import subprocess
from dataclasses import dataclass
from typing import Dict, List

from utils import TypeEnum, TypeSpec, MethodDef, json_default_val, ClassDef

CPP_TYPE_SPECS: Dict[TypeEnum, TypeSpec] = {
    TypeEnum.BOOL: TypeSpec('bool', 'false', 'des_bool', 'ser_bool'),
    TypeEnum.INT: TypeSpec('int', '0', 'des_int', 'ser_int'),
    TypeEnum.LONG: TypeSpec('long long', '0', 'des_long', 'ser_long'),
    TypeEnum.DOUBLE: TypeSpec('double', '0.0', 'des_double', 'ser_double'),
    TypeEnum.STRING: TypeSpec('string', '""', 'des_string', 'ser_string'),
    TypeEnum.INT_LIST: TypeSpec('vector<int>', 'vector<int>()', 'des_int_list', 'ser_int_list'),
    TypeEnum.INT_LIST_LIST: TypeSpec('vector<vector<int>>', 'vector<vector<int>>()', 'des_int_list_list', 'ser_int_list_list'),
    TypeEnum.DOUBLE_LIST: TypeSpec('vector<double>', 'vector<double>()', 'des_double_list', 'ser_double_list'),
    TypeEnum.STRING_LIST: TypeSpec('vector<string>', 'vector<string>()', 'des_string_list', 'ser_string_list'),
    TypeEnum.BOOL_LIST: TypeSpec('vector<bool>', 'vector<bool>()', 'des_bool_list', 'ser_bool_list'),
    TypeEnum.TREENODE: TypeSpec('TreeNode*', 'nullptr', 'des_tree', 'ser_tree'),
    TypeEnum.LISTNODE: TypeSpec('ListNode*', 'nullptr', 'des_linked_list', 'ser_linked_list'),
    TypeEnum.LONG_LIST: TypeSpec('vector<long long>', 'vector<long long>()', 'des_long_list', 'ser_long_list'),
    TypeEnum.NONE: TypeSpec('void', '/*none*/', 'des_none', 'ser_none'),
}

TIME_COST_PATH = 'time_cost.txt'


@dataclass
class CppMethodDef(MethodDef):
    def generate(self) -> str:
        params_list: List[str] = []
        for p_type, p_name in zip(self.params_type, self.params_name):
            t = CPP_TYPE_SPECS[p_type].lang_type
            params_list.append(f"{t} {p_name}")
        ret_type = CPP_TYPE_SPECS[self.return_type].lang_type
        signature = f"{ret_type} {self.function_name}({', '.join(params_list)})"
        return signature


@dataclass
class CppClassDef(ClassDef):
    def __post_init__(self):
        self.constructor.function_name = self.name
        self.constructor.return_type = TypeEnum.NONE

    def constructor_generate(self):
        params_list: List[str] = []
        for p_type, p_name in zip(self.constructor.params_type, self.constructor.params_name):
            t = CPP_TYPE_SPECS[p_type].lang_type
            params_list.append(f"{t} {p_name}")
        signature = f"{self.name}({', '.join(params_list)})"
        return signature


# Generate user class skeleton for design-style problems.
def cpp_generate_system_code(class_def: CppClassDef) -> str:
    lines = [
        f'class {class_def.name}{{',
        'public:',
        f'    {class_def.constructor_generate()}{{',
        '        // write code here',
        '    }',
        ''
    ]
    for method_def in class_def.methods:
        lines += [
            f'    {method_def.generate()}{{',
            '        // write code here',
            ('        return;' if method_def.return_type == TypeEnum.NONE else
             f'        return {CPP_TYPE_SPECS[method_def.return_type].default};'),
            '    }',
            ''
        ]
    lines += [
        '};',
        ''
    ]
    return "\n".join(lines)


def cpp_generate_solution_code(method_def: CppMethodDef):
    lines = [
        'class Solution{',
        'public:',
        f'    {method_def.generate()}{{',
        '        // write code here',
        f'        return {CPP_TYPE_SPECS[method_def.return_type].default};',
        '    }',
        '};'
    ]
    return "\n".join(lines)


# Generate runner for classic function-style problems.
def cpp_generate_trailer_code(method_def: CppMethodDef):
    params_num = len(method_def.params_name)
    lines_pre = []
    for i, (p_type, p_name) in enumerate(zip(method_def.params_type, method_def.params_name)):
        lines_pre += [
            'json_str = reader.read_line();',
            'if(json_str.empty()){',
            '    break;' if i == 0 else f'    throw std::invalid_argument("Testcase is missing the required argument: `{p_name}`");',
            '}',
            f"{CPP_TYPE_SPECS[p_type].lang_type} p{i} = {CPP_TYPE_SPECS[p_type].des_func}(json_str);"
        ]
    lines = [
        '',
        'void run() {',
        '    StdinWrapper reader;',
        '    StdoutWrapper writer;',
        '    string json_str;',
        '    clock_t total_time = 0;',
        '    while (true) {',
        '',
        '\n'.join([' ' * 8 + s for s in lines_pre]),
        '',
        '        unsigned long long start_stamp = __get_cpu_time();',
        f'        {CPP_TYPE_SPECS[method_def.return_type].lang_type} result = Solution().{method_def.function_name}({", ".join(f"p{x}" for x in range(params_num))});',
        '        unsigned long long end_stamp = __get_cpu_time();',
        '        total_time += (end_stamp - start_stamp);',
        f'        string result_str = {CPP_TYPE_SPECS[method_def.return_type].ser_func}(result);',
        '        writer.write_line(result_str);',
        '    }',
        '',
        f'    std::ofstream fp("{TIME_COST_PATH}");',
        '    fp << total_time / 100000UL;',
        '}',
        '',
        'int main() {',
        '    try {',
        '        run();',
        '    } catch (const std::exception& e) {',
        '        std::cerr << e.what() << std::endl;',
        '        return 1;',
        '    }',
        '    return 0;',
        '}'
    ]

    return "\n".join(lines)


# Build dispatch logic that converts raw JSON params to typed values.
def _cpp_generate_system_dispatch_block(method_defs: List[CppMethodDef], class_name: str) -> str:
    lines: List[str] = []
    for idx, method_def in enumerate(method_defs):
        branch = 'if' if idx == 0 else 'else if'
        lines.append(f'        {branch} (method == "{method_def.function_name}") {{')
        lines.append(f'            if (params_cur.size() != {len(method_def.params_type)}) {{')
        lines.append(f'                throw std::invalid_argument("Method `{method_def.function_name}` argument size mismatch.");')
        lines.append('            }')

        for p_idx, p_type in enumerate(method_def.params_type):
            spec = CPP_TYPE_SPECS[p_type]
            lines.append(f'            {spec.lang_type} p{p_idx} = {spec.des_func}(params_cur[{p_idx}]);')

        args = ', '.join(f'p{i}' for i in range(len(method_def.params_type)))
        lines.append('            unsigned long long start_stamp = __get_cpu_time();')

        if method_def.return_type == TypeEnum.NONE:
            lines.append(f'            obj->{method_def.function_name}({args});')
            lines.append('            unsigned long long end_stamp = __get_cpu_time();')
            lines.append('            ctime_total += (end_stamp - start_stamp);')
            lines.append('            return "null";')
        else:
            ret_spec = CPP_TYPE_SPECS[method_def.return_type]
            lines.append(f'            {ret_spec.lang_type} ret = obj->{method_def.function_name}({args});')
            lines.append('            unsigned long long end_stamp = __get_cpu_time();')
            lines.append('            ctime_total += (end_stamp - start_stamp);')
            lines.append(f'            return {ret_spec.ser_func}(ret);')

        lines.append('        }')

    lines.append('        else {')
    lines.append('            throw std::invalid_argument("Input method does not exist.");')
    lines.append('        }')
    return "\n".join(lines)


# Generate driver for LeetCode-style system design IO (methods + params).
def cpp_generate_system_trailer_code(class_def: CppClassDef) -> str:
    ctor = class_def.constructor
    ctor_param_count = len(ctor.params_type)
    ctor_parse_lines = [
        f'        if (params[0].size() != {ctor_param_count}) {{',
        '            throw std::invalid_argument("Constructor argument size mismatch.");',
        '        }'
    ]
    for idx, p_type in enumerate(ctor.params_type):
        spec = CPP_TYPE_SPECS[p_type]
        ctor_parse_lines.append(f'        {spec.lang_type} ctor_p{idx} = {spec.des_func}(params[0][{idx}]);')

    ctor_args = ', '.join(f'ctor_p{i}' for i in range(ctor_param_count))
    dispatch_block = _cpp_generate_system_dispatch_block(class_def.methods, class_def.name)

    lines = [
        '',
        'class DriverSystemSolution {',
        'public:',
        '    unsigned long long ctime_total = 0;',
        '',
        '    static string join_json(const vector<string>& elements) {',
        '        if (elements.empty()) {',
        '            return "";',
        '        }',
        '        string result = elements[0];',
        '        for (size_t i = 1; i < elements.size(); ++i) {',
        '            result += ",";',
        '            result += elements[i];',
        '        }',
        '        return result;',
        '    }',
        '',
        f'    string dispatch(const string& method, const vector<string>& params_cur, {class_def.name}* obj) {{',
        dispatch_block,
        '    }',
        '',
        '    string solve(const vector<string>& methods, const vector<vector<string>>& params) {',
        '        if (methods.empty() || params.empty() || methods.size() != params.size()) {',
        '            throw std::invalid_argument("Input methods size does not equal to params size or equals to 0.");',
        '        }',
        f'        if (methods[0] != "{class_def.name}") {{',
        '            throw std::invalid_argument("First method is not constructor.");',
        '        }',
        '\n'.join(ctor_parse_lines),
        '        unsigned long long ctor_start_stamp = __get_cpu_time();',
        f'        std::unique_ptr<{class_def.name}> obj(new {class_def.name}({ctor_args}));',
        '        unsigned long long ctor_end_stamp = __get_cpu_time();',
        '        ctime_total += (ctor_end_stamp - ctor_start_stamp);',
        '',
        '        vector<string> outputs;',
        '        outputs.reserve(methods.size());',
        '        outputs.push_back("null");',
        '        for (size_t i = 1; i < methods.size(); ++i) {',
        '            outputs.push_back(dispatch(methods[i], params[i], obj.get()));',
        '        }',
        '        return "[" + join_json(outputs) + "]";',
        '    }',
        '};',
        '',
        'void run() {',
        '    StdinWrapper reader;',
        '    StdoutWrapper writer;',
        '    DriverSystemSolution driver;',
        '    while (true) {',
        '        string line_methods = reader.read_line();',
        '        if (line_methods.empty()) {',
        '            break;',
        '        }',
        '        string line_params = reader.read_line();',
        '        if (line_params.empty()) {',
        '            throw std::invalid_argument("Testcase is missing the required argument: `params`");',
        '        }',
        '        vector<string> methods = des_string_list(line_methods);',
        '        vector<vector<string>> params = des_json_value_list_list(line_params);',
        '        writer.write_line(driver.solve(methods, params));',
        '    }',
        f'    std::ofstream fp("{TIME_COST_PATH}");',
        '    fp << driver.ctime_total / 100000UL;',
        '}',
        '',
        'int main() {',
        '    try {',
        '        run();',
        '    } catch (const std::exception& e) {',
        '        std::cerr << e.what() << std::endl;',
        '        return 1;',
        '    }',
        '    return 0;',
        '}',
    ]

    return "\n".join(lines)


def cpp_test(method_def: CppMethodDef):
    try:
        TMP = 'tmp'
        PATH = 'cpp'

        os.makedirs(TMP, exist_ok=True)
        with open(os.path.join(TMP, 'user.in'), 'w') as fp:
            for p_type in method_def.params_type:
                fp.write(json_default_val[p_type] + '\n')

        solution_code = cpp_generate_solution_code(method_def)
        trailer_code = cpp_generate_trailer_code(method_def)

        with open(os.path.join(TMP, 'main.cpp'), 'w') as fp:
            with open(os.path.join(PATH, 'cpp_header')) as fq:
                fp.write(fq.read() + '\n' + solution_code + trailer_code)

        tmp_list = [filename for filename in os.listdir(PATH) if filename.startswith('libcpp_') and filename.endswith('.so')]
        current_dir = os.getcwd()
        if len(tmp_list) == 0:
            print(f"No files matching the condition were found in the {PATH} directory. Running the build command...")
            os.chdir(PATH)
            subprocess.run(['g++', '-shared', '-o', 'libcpp_parse_tools.so', '-fPIC', 'cpp_parse_tools.cpp', 'cpp_parse_module.cpp', '../rapidjson_helper.cpp'])
            os.chdir(current_dir)
        else:
            print(f"{tmp_list[0]} already exists in the {PATH} directory. No need to run the build command.")

        for filename in ['cpp_io_tools.h', 'cpp_node_type.h', 'cpp_parse_tools.h', 'cpp_parse_module.h', 'libcpp_parse_tools.so']:
            src = os.path.join(PATH, filename)
            dst = os.path.join(TMP, filename)
            shutil.copy(src, dst)

        os.chdir(TMP)
        result = subprocess.run(['g++', '-o', 'main', 'main.cpp', '-L.', '-lcpp_parse_tools', '-Wl,-rpath=.'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)

        if result.returncode != 0:
            return result.returncode, result.stderr

        result = subprocess.run(['./main'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)
        if result.returncode != 0:
            return result.returncode, result.stderr

        os.chdir(current_dir)

        required_files = ['user.out', 'time_cost.txt']
        files_in_directory = os.listdir(TMP)

        missing_files = [file for file in required_files if file not in files_in_directory]
        if missing_files:
            return 1, f"Missing these files: {', '.join(missing_files)}"
        return 0, {'main_body.cpp': solution_code, 'main_trailer.cpp': trailer_code}
    finally:
        shutil.rmtree(TMP)


if __name__ == '__main__':
    params_type = [TypeEnum.INT, TypeEnum.LONG, TypeEnum.DOUBLE, TypeEnum.STRING, TypeEnum.INT_LIST,
                   TypeEnum.INT_LIST_LIST, TypeEnum.DOUBLE_LIST, TypeEnum.STRING_LIST, TypeEnum.BOOL_LIST,
                   TypeEnum.BOOL, TypeEnum.TREENODE, TypeEnum.LISTNODE]
    params_name = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']
    return_type = TypeEnum.INT_LIST_LIST
    m1 = CppMethodDef('solve', params_type, params_name, return_type)
    print(cpp_generate_solution_code(m1))
    m2 = CppMethodDef('solve2', params_type, params_name, TypeEnum.INT)
    m3 = CppMethodDef('solve2', params_type, params_name, TypeEnum.INT)
    class_def = CppClassDef('System', m3, [m1, m2])
    print(cpp_generate_system_code(class_def))
    print(cpp_generate_trailer_code(m1))
    print(cpp_generate_system_trailer_code(class_def))


