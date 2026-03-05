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


TIME_COST_PATH = 'time_cost.txt'

def cpp_generate_system_code(class_def: CppClassDef) -> str:
    lines = [
        f'class {class_def.name}{{',
        f'public:',
        f'    {class_def.constructor_generate()}{{',
        f'        // write code here',
        f'        return;',
        f'    }}',
        f''
    ]
    for method_def in class_def.methods:
        lines += [
            f'    {method_def.generate()}{{',
            f'        // write code here',
            f'        return {CPP_TYPE_SPECS[method_def.return_type].default};',
            f'    }}',
            ''
        ]
    lines += [
        f'}};\n'
    ]
    return "\n".join(lines)


def cpp_generate_solution_code(method_def : CppMethodDef):
    lines = [
        'class Solution{',
        'public:',
        f"    {method_def.generate()}{{",
        '        // write code here',
        f'        return {CPP_TYPE_SPECS[method_def.return_type].default};',
        '    }',
        '};'
    ]
    return "\n".join(lines)


def cpp_generate_trailer_code(method_def : CppMethodDef):
    params_num = len(params_name)
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
        '    ',
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

def cpp_test(method_def : CppMethodDef):
    try:
        TMP = 'tmp'
        PATH = 'cpp'

        os.makedirs(TMP, exist_ok=True)
        with open(os.path.join(TMP, 'user.in'),'w') as fp:
            for p_type in params_type:
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
        return 0, {'main_body.cpp' : solution_code, 'main_trailer.cpp' : trailer_code}
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
    m1 = CppMethodDef('solve', params_type, params_name, return_type)
    m2 = CppMethodDef('solve2', params_type, params_name, TypeEnum.INT)
    m3 = CppMethodDef('solve2', params_type, params_name, TypeEnum.INT)
    # print(m2)
    print(cpp_generate_system_code(CppClassDef("System", m3, [m1, m2])))
    print(cpp_generate_trailer_code(m1))
