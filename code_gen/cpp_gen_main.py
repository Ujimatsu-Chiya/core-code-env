import os
import shutil
import subprocess
from typing import List
from utils import TypeEnum, json_default_val

cpp_type = {
    TypeEnum.BOOL: 'bool',
    TypeEnum.INT: 'int',
    TypeEnum.LONG: 'long long',
    TypeEnum.DOUBLE: 'double',
    TypeEnum.STRING: 'string',
    TypeEnum.INT_LIST: 'vector<int>',
    TypeEnum.INT_LIST_LIST: 'vector<vector<int>>',
    TypeEnum.DOUBLE_LIST: 'vector<double>',
    TypeEnum.STRING_LIST: 'vector<string>',
    TypeEnum.BOOL_LIST: 'vector<bool>',
    TypeEnum.TREENODE: 'TreeNode*',
    TypeEnum.LISTNODE: 'ListNode*',
    TypeEnum.LONG_LIST: 'vector<long long>'
}

cpp_default_val = {
    TypeEnum.BOOL: 'false',
    TypeEnum.INT: '0',
    TypeEnum.LONG: '0',
    TypeEnum.DOUBLE: '0.0',
    TypeEnum.STRING: '""',
    TypeEnum.INT_LIST: 'vector<int>()',
    TypeEnum.INT_LIST_LIST: 'vector<vector<int>>()',
    TypeEnum.DOUBLE_LIST: 'vector<double>()',
    TypeEnum.STRING_LIST: 'vector<string>()',
    TypeEnum.BOOL_LIST: 'vector<bool>()',
    TypeEnum.TREENODE: 'nullptr',
    TypeEnum.LISTNODE: 'nullptr',
    TypeEnum.LONG_LIST: 'vector<long long>()'
}

des_func_name = {
    TypeEnum.BOOL : 'des_bool',
    TypeEnum.INT : 'des_int',
    TypeEnum.LONG : 'des_long',
    TypeEnum.DOUBLE : 'des_double',
    TypeEnum.STRING: 'des_string',
    TypeEnum.INT_LIST: 'des_int_list',
    TypeEnum.INT_LIST_LIST: 'des_int_list_list',
    TypeEnum.DOUBLE_LIST: 'des_double_list',
    TypeEnum.STRING_LIST: 'des_string_list',
    TypeEnum.BOOL_LIST: 'des_bool_list',
    TypeEnum.TREENODE: 'des_tree',
    TypeEnum.LISTNODE: 'des_linked_list',
    TypeEnum.LONG_LIST : 'des_long_list'
}

ser_func_name = {
    TypeEnum.BOOL : 'ser_bool',
    TypeEnum.INT : 'ser_int',
    TypeEnum.LONG : 'ser_long',
    TypeEnum.DOUBLE : 'ser_double',
    TypeEnum.STRING: 'ser_string',
    TypeEnum.INT_LIST: 'ser_int_list',
    TypeEnum.INT_LIST_LIST: 'ser_int_list_list',
    TypeEnum.DOUBLE_LIST: 'ser_double_list',
    TypeEnum.STRING_LIST: 'ser_string_list',
    TypeEnum.BOOL_LIST: 'ser_bool_list',
    TypeEnum.TREENODE: 'ser_tree',
    TypeEnum.LISTNODE: 'ser_linked_list',
    TypeEnum.LONG_LIST : 'ser_long_list'
}

TIME_COST_PATH = 'time_cost.txt'

def _cpp_generate_signature(function_name:str, params_type:List[TypeEnum], params_name:List[str], return_type:TypeEnum) -> str:
    params_list = []
    for p_type, p_name in zip(params_type, params_name):
        p_type_str = cpp_type[p_type]
        params_list.append(f'{p_type_str} {p_name}')
    cpp_signature = f"{cpp_type[return_type]} {function_name}({', '.join(params_list)})"
    return cpp_signature

def cpp_generate_solution_code(function_name:str, params_type:List[TypeEnum], params_name:List[str], return_type:TypeEnum):
    lines = [
        'class Solution{',
        'public:',
        f"    {_cpp_generate_signature(function_name, params_type, params_name, return_type)}{{",
        '        // write code here',
        f'        return {cpp_default_val[return_type]};',
        '    }',
        '};'
    ]
    return "\n".join(lines)


def cpp_generate_trailer_code(function_name:str, params_type:List[TypeEnum], params_name:List[str], return_type:TypeEnum):
    params_num = len(params_name)
    lines_pre = []
    for i, (p_type, p_name) in enumerate(zip(params_type, params_name)):
            lines_pre += [
                 'json_str = reader.read_line();',
                 'if(json_str == nullptr){',
                 '    break;' if i == 0 else f'    throw std::invalid_argument("Testcase is missing the required argument: `{p_name}`");',
                 '}',
                 f"{cpp_type[p_type]} p{i} = {des_func_name[p_type]}(json_str);"
            ]
    lines = [
        '',
        'void run() {',
        '    StdinWrapper reader;',
        '    StdoutWrapper writer;',
        '    char *json_str = nullptr;',
        '    clock_t total_time = 0;',
        '    while (true) {',
        '',
        '\n'.join([' ' * 8 + s for s in lines_pre]),
        '',
        '        unsigned long long start_stamp = __get_cpu_time();',
        f'        {cpp_type[return_type]} result = Solution().{function_name}({", ".join(f"p{x}" for x in range(params_num))});',
        '        unsigned long long end_stamp = __get_cpu_time();',
        '        total_time += (end_stamp - start_stamp);',
        f'        char *result_str = {ser_func_name[return_type]}(result);',
        '        writer.write_line(result_str);',
        '        delete[] result_str;',
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

def cpp_test(function_name:str, params_type:List[TypeEnum], params_name:List[str], return_type:TypeEnum):
    try:
        TMP = 'tmp'
        PATH = 'cpp'

        os.makedirs(TMP, exist_ok=True)
        with open(os.path.join(TMP, 'user.in'),'w') as fp:
            for p_type in params_type:
                fp.write(json_default_val[p_type] + '\n')

        
    
        solution_code = cpp_generate_solution_code(function_name, params_type, params_name, return_type)
        trailer_code = cpp_generate_trailer_code(function_name, params_type, params_name, return_type)

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
    print(cpp_test('solve', params_type, params_name, return_type)[1])