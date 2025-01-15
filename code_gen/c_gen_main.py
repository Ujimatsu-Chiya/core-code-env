import os
import shutil
import subprocess
from typing import List
from utils import TypeEnum, json_default_val

c_type = {
    TypeEnum.BOOL: 'bool',
    TypeEnum.INT: 'int',
    TypeEnum.LONG: 'long long',
    TypeEnum.DOUBLE: 'double',
    TypeEnum.STRING: 'char*',
    TypeEnum.INT_LIST: 'int*',
    TypeEnum.INT_LIST_LIST: 'int**',
    TypeEnum.DOUBLE_LIST: 'double*',
    TypeEnum.STRING_LIST: 'char**',
    TypeEnum.BOOL_LIST: 'bool*',
    TypeEnum.TREENODE: 'struct TreeNode*',
    TypeEnum.LISTNODE: 'struct ListNode*',
    TypeEnum.LONG_LIST: 'long long*'
}

c_default_val = {
    TypeEnum.BOOL: 'false',
    TypeEnum.INT: '0',
    TypeEnum.LONG: '0',
    TypeEnum.DOUBLE: '0.0',
    TypeEnum.STRING: 'NULL',
    TypeEnum.INT_LIST: 'NULL',
    TypeEnum.INT_LIST_LIST: 'NULL',
    TypeEnum.DOUBLE_LIST: 'NULL',
    TypeEnum.STRING_LIST: 'NULL',
    TypeEnum.BOOL_LIST: 'NULL',
    TypeEnum.TREENODE: 'NULL',
    TypeEnum.LISTNODE: 'NULL',
    TypeEnum.LONG_LIST: 'NULL'
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

delete_func_name = {
    TypeEnum.INT_LIST: 'delete_int_list',
    TypeEnum.INT_LIST_LIST: 'delete_int_list_list',
    TypeEnum.DOUBLE_LIST: 'delete_double_list',
    TypeEnum.STRING_LIST: 'delete_string_list',
    TypeEnum.BOOL_LIST: 'delete_bool_list',
    TypeEnum.TREENODE: 'delete_tree',
    TypeEnum.LISTNODE: 'delete_linked_list',
    TypeEnum.LONG_LIST : 'delete_long_list',
    TypeEnum.STRING: 'delete_string'
}


TIME_COST_PATH = 'time_cost.txt'

def _generate_c_signature(function_name:str, params_type:List[TypeEnum], params_name:List[str], return_type:TypeEnum) -> str:
    params_list = []
    for p_type, p_name in zip(params_type, params_name):
        p_type_str = c_type[p_type]
        params_list.append(f'{p_type_str} {p_name}')
        if TypeEnum.get_dimension(p_type) == 1:
            params_list.append(f'size_t {p_name + "_size"}')
        elif TypeEnum.get_dimension(p_type) == 2:
            params_list.append(f'size_t {p_name + "_rows"}')
            params_list.append(f'size_t* {p_name + "_cols"}')

    if TypeEnum.get_dimension(return_type) == 1:
        params_list.append(f'size_t* result_size')
    elif TypeEnum.get_dimension(return_type) == 2:
        params_list.append(f'size_t* result_rows')
        params_list.append(f'size_t** result_cols')
    c_signature = f'{c_type[return_type]} {function_name}({", ".join(params_list)})'
    return c_signature

def c_generate_solution_code(function_name:str, params_type:List[TypeEnum], params_name:List[str], return_type:TypeEnum):
    lines = [
        f'{_generate_c_signature(function_name, params_type, params_name, return_type)}{{',
        '    // write code here',
        f'    return {c_default_val[return_type]};',
        '}'
    ]
    return '\n'.join(lines)



def c_generate_trailer_code(function_name:str, params_type:List[TypeEnum], params_name:List[str], return_type:TypeEnum):
    lines_pre = []
    arguments_list = []
    lines_delete = []
    for i, (p_type, p_name) in enumerate(zip(params_type, params_name)):
            lines_pre += [
                'json_str = read_line(reader);',
                'if (json_str == NULL) {',
            ] + ([
                '    break;'
            ] if i == 0 else [
                f'    fprintf(stderr, "Testcase is missing the required argument: `{p_name}`");',
                '    exit(1);',
            ]) + [
                '}'     
            ]
                
            if TypeEnum.get_dimension(p_type) == 0:
                lines_pre += [
                    f'{c_type[p_type]} p{i} = {des_func_name[p_type]}(json_str);'
                ]
                arguments_list.append(f'p{i}')
                if p_type in [TypeEnum.LISTNODE, TypeEnum.TREENODE, TypeEnum.STRING]:
                    lines_delete.append(f'{delete_func_name[p_type]}(p{i});')
            elif TypeEnum.get_dimension(p_type) == 1:
                lines_pre += [
                    f'size_t p{i}_size;',
                    f'{c_type[p_type]} p{i} = {des_func_name[p_type]}(json_str, &p{i}_size);'
                ]
                arguments_list.extend([f'p{i}, p{i}_size'])
                if p_type in [TypeEnum.STRING_LIST]:
                    lines_delete.append(f'{delete_func_name[p_type]}(p{i}, p{i}_size);',)
                else:
                    lines_delete.append(f'{delete_func_name[p_type]}(p{i});')
            elif TypeEnum.get_dimension(p_type) == 2:
                lines_pre += [
                    f'size_t p{i}_rows;',
                    f'size_t* p{i}_cols = NULL;',
                    f'{c_type[p_type]} p{i} = {des_func_name[p_type]}(json_str, &p{i}_rows, &p{i}_cols);'
                ]
                arguments_list.extend([f'p{i}, p{i}_rows, p{i}_cols'])
                lines_delete.extend([
                    f'{delete_func_name[p_type]}(p{i}, p{i}_rows);',
                    f'delete_size_t_list(p{i}_cols);'
                    ])
    
    lines_result_defined = []
    if TypeEnum.get_dimension(return_type) == 1:
        arguments_list.append('&result_size')
        lines_result_defined.append('size_t result_size;')
        if p_type in [TypeEnum.STRING_LIST]:
            lines_delete.append(f'{delete_func_name[return_type]}(p{i}, p{i}_size);')
        else:
            lines_delete.append(f'{delete_func_name[return_type]}(p{i});')
        
    elif TypeEnum.get_dimension(return_type) == 2:
        arguments_list.extend(['&result_rows', '&result_cols'])
        lines_result_defined.extend(['size_t result_rows;','size_t* result_cols = NULL;'])
        lines_delete.extend([
                    f'{delete_func_name[return_type]}(result, result_rows);',
                    'delete_size_t_list(result_cols);'
                    ])
    
    lines = [
        '',
        'void run() {',
        '    StdinWrapper* reader = create_stdin_wrapper();',
        '    StdoutWrapper* writer = create_stdout_wrapper();',
        '    char *json_str = NULL;',
        '    clock_t total_time = 0;',
        '\n'.join([' ' * 4 + s for s in lines_result_defined]),
        '',
        '    while (true) {',
        '',
        '\n'.join([' ' * 8 + s for s in lines_pre]),
        '',
        '        unsigned long long start_stamp = __get_cpu_time();',
        f'        {c_type[return_type]} result = {function_name}({", ".join(arguments_list)});',
        '        unsigned long long end_stamp = __get_cpu_time();',
        '        total_time += (end_stamp - start_stamp);',
        '        ' + (f'char *result_str = {ser_func_name[return_type]}(result);' if TypeEnum.get_dimension(return_type) == 0 else
                      f'char *result_str = {ser_func_name[return_type]}((const {c_type[return_type]})result, result_size);' if  TypeEnum.get_dimension(return_type) == 1 else 
                      f'char *result_str = {ser_func_name[return_type]}((const {c_type[return_type]})result, result_rows, result_cols);'
                      ),
        '        write_line(writer, result_str);',
        '\n'.join([' ' * 8 + s for s in lines_delete]),
        f'        {delete_func_name[TypeEnum.STRING]}(result_str);',
        '    }',
        '    ',
        '    delete_stdin_wrapper(reader);',
        '    delete_stdout_wrapper(writer);',
        f'    FILE *fp = fopen("{TIME_COST_PATH}", "w");',
        '    fprintf(fp, "%lu", total_time / 100000UL);',
        '    fclose(fp);',
        '}',
        '',
        'int main() {',
        '    run();',
        '    return 0;',
        '}'
    ]

    return "\n".join(lines)

def c_test(function_name:str, params_type:List[TypeEnum], params_name:List[str], return_type:TypeEnum):
    try:
        TMP = 'tmp'
        PATH = 'c'

        os.makedirs(TMP, exist_ok=True)
        with open(os.path.join(TMP, 'user.in'),'w') as fp:
            for p_type in params_type:
                fp.write(json_default_val[p_type] + '\n')

        
        solution_code = c_generate_solution_code(function_name, params_type, params_name, return_type)
        trailer_code = c_generate_trailer_code(function_name, params_type, params_name, return_type)

        with open(os.path.join(TMP, 'main.c'), 'w') as fp:
            with open(os.path.join(PATH, 'c_header')) as fq:
                fp.write(fq.read() + '\n' + solution_code + trailer_code)

        tmp_list = [filename for filename in os.listdir(PATH) if filename.startswith('libc') and filename.endswith('.so')]
        current_dir = os.getcwd()
        if len(tmp_list) == 0:
            print(f"No files matching the condition were found in the {PATH} directory. Running the build command...")
            os.chdir(PATH)
            subprocess.run(['g++', '-shared', '-o', 'libc_parse_tools.so', '-fPIC', 'c_parse_tools.c', 'c_parse_module.cpp', '../rapidjson_helper.cpp'])
            os.chdir(current_dir)
        else:
            print(f"{tmp_list[0]} already exists in the {PATH} directory. No need to run the build command.")

        for filename in ['c_io_tools.h', 'c_io_tools.c', 'c_node_type.h', 'c_parse_tools.h', 'c_parse_module.h', 'libc_parse_tools.so']:
            src = os.path.join(PATH, filename)
            dst = os.path.join(TMP, filename)
            shutil.copy(src, dst)
    
        os.chdir(TMP)
        result = subprocess.run(['gcc', '-o', 'main', 'main.c', 'c_io_tools.c', '-L.', '-lc_parse_tools', '-Wl,-rpath=.'],
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
        return 0, {'main_body.c' : solution_code, 'main_trailer.c' : trailer_code}
    finally:
        shutil.rmtree(TMP)
        pass

if __name__ == '__main__':
    params_type = [TypeEnum.INT, TypeEnum.LONG, TypeEnum.DOUBLE, TypeEnum.STRING, TypeEnum.INT_LIST,
                   TypeEnum.INT_LIST_LIST, TypeEnum.DOUBLE_LIST, TypeEnum.STRING_LIST, TypeEnum.BOOL_LIST,
                   TypeEnum.BOOL, TypeEnum.TREENODE, TypeEnum.LISTNODE]
    params_name = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']
    return_type = TypeEnum.INT_LIST_LIST
    print(c_test('solve', params_type, params_name, return_type))