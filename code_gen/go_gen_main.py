import os
import shutil
import subprocess
from typing import List
from utils import TypeEnum, json_default_val

go_type = {
    TypeEnum.BOOL: 'bool',
    TypeEnum.INT: 'int',
    TypeEnum.LONG: 'int64',
    TypeEnum.DOUBLE: 'float64',
    TypeEnum.STRING: 'string',
    TypeEnum.INT_LIST: '[]int',
    TypeEnum.INT_LIST_LIST: '[][]int',
    TypeEnum.DOUBLE_LIST: '[]float64',
    TypeEnum.STRING_LIST: '[]string',
    TypeEnum.BOOL_LIST: '[]bool',
    TypeEnum.TREENODE: '*TreeNode',
    TypeEnum.LISTNODE: '*ListNode',
    TypeEnum.LONG_LIST: '[]int64'
}

go_default_val = {
    TypeEnum.BOOL: 'false',
    TypeEnum.INT: '0',
    TypeEnum.LONG: '0',
    TypeEnum.DOUBLE: '0.0',
    TypeEnum.STRING: '""',
    TypeEnum.INT_LIST: '[]int{}',
    TypeEnum.INT_LIST_LIST: '[][]int{}',
    TypeEnum.DOUBLE_LIST: '[]float64{}',
    TypeEnum.STRING_LIST: '[]string{}',
    TypeEnum.BOOL_LIST: '[]bool{}',
    TypeEnum.TREENODE: 'nil',
    TypeEnum.LISTNODE: 'nil',
    TypeEnum.LONG_LIST: '[]int64{}'
}


des_func_name = {
    TypeEnum.BOOL : 'DesBool',
    TypeEnum.INT : 'DesInt',
    TypeEnum.LONG : 'DesLong',
    TypeEnum.DOUBLE : 'DesDouble',
    TypeEnum.STRING: 'DesString',
    TypeEnum.INT_LIST: 'DesIntList',
    TypeEnum.INT_LIST_LIST: 'DesIntListList',
    TypeEnum.DOUBLE_LIST: 'DesDoubleList',
    TypeEnum.STRING_LIST: 'DesStringList',
    TypeEnum.BOOL_LIST: 'DesBoolList',
    TypeEnum.TREENODE: 'DesTree',
    TypeEnum.LISTNODE: 'DesLinkedList',
    TypeEnum.LONG_LIST : 'DesLongList'
}

ser_func_name = {
    TypeEnum.BOOL : 'SerBool',
    TypeEnum.INT : 'SerInt',
    TypeEnum.LONG : 'SerLong',
    TypeEnum.DOUBLE : 'SerDouble',
    TypeEnum.STRING: 'SerString',
    TypeEnum.INT_LIST: 'SerIntList',
    TypeEnum.INT_LIST_LIST: 'SerIntListList',
    TypeEnum.DOUBLE_LIST: 'SerDoubleList',
    TypeEnum.STRING_LIST: 'SerStringList',
    TypeEnum.BOOL_LIST: 'SerBoolList',
    TypeEnum.TREENODE: 'SerTree',
    TypeEnum.LISTNODE: 'SerLinkedList',
    TypeEnum.LONG_LIST : 'SerLongList'
}

TIME_COST_PATH = 'time_cost.txt'

def _go_generate_signature(function_name:str, params_type:List[TypeEnum], params_name:List[str], return_type:TypeEnum) -> str:
    params_list = []
    for p_type, p_name in zip(params_type, params_name):
        p_type_str = go_type[p_type]
        params_list.append(f'{p_name} {p_type_str}')
    go_signature = f"func {function_name}({', '.join(params_list)}) {go_type[return_type]}"
    return go_signature



def go_generate_solution_code(function_name:str, params_type:List[TypeEnum], params_name:List[str], return_type:TypeEnum):
    lines = [
        '',
        f"{_go_generate_signature(function_name, params_type, params_name, return_type)} {{",
        '    // write code here',
        f'    return {go_default_val[return_type]};',
        '}',
        ''
    ]
    return "\n".join(lines)


def go_generate_trailer_code(function_name:str, params_type:List[TypeEnum], params_name:List[str], return_type:TypeEnum):
    params_num = len(params_name)
    lines_pre = []
    for i, (p_type, p_name) in enumerate(zip(params_type, params_name)):
            lines_pre += [
                '',
                f'jsonStr {":=" if i == 0 else "="} reader.ReadLine()',
                'if jsonStr == "" {',
            ] + ([
                '    break'
            ] if i == 0 else [
                f'    fmt.Fprintf(os.Stderr, "Testcase is missing the required argument: `{p_name}`")',
                '    os.Exit(1)',
            ]) + [
                '}',
                f'p{i} := {des_func_name[p_type]}(jsonStr)'
            ]
    lines = [
        '',
        'func Run() {',
        '    reader := CreateStdinWrapper()',
        '    writer := CreateStdoutWrapper()',
        '',
        '    totalTime := int64(0)',
        '',
        '    for {',
        '\n'.join([' ' * 8 + s for s in lines_pre]),
        '',
        '        startStamp := GetCPUTime()',
        '',
        f'        result := {function_name}({", ".join(f"p{x}" for x in range(params_num))})',
        '',
        '        endStamp := GetCPUTime()',
        '        totalTime += endStamp - startStamp',
        '',
        f'        writer.WriteLine({ser_func_name[return_type]}(result))',
        '    }',
        '',
        f'    timeCostFile, err := os.Create("{TIME_COST_PATH}")',
        '    if err != nil {',
        '        fmt.Fprintf(os.Stderr, "Error creating time cost file: %v", err)',
        '        os.Exit(1)',
        '    }',
        '    fmt.Fprintf(timeCostFile, "%d", totalTime / 1000000)',
        '    if err != nil {',
        '        fmt.Fprintf(os.Stderr, "Error writing to output file: %v", err)',
        '        os.Exit(1)',
        '    }',
        '    if err != nil {',
        '        fmt.Fprintf(os.Stderr, "Error flushing output file: %v", err)',
        '        os.Exit(1)',
        '    }',
        '}',
        '',
        'func main(){',
        '    Run()',
        '}'
    ]
    
    return "\n".join(lines)


def go_test(function_name:str, params_type:List[TypeEnum], params_name:List[str], return_type:TypeEnum):
    try:
        TMP = 'tmp'
        PATH = 'go'

        os.makedirs(TMP, exist_ok=True)
        with open(os.path.join(TMP, 'user.in'),'w') as fp:
            for p_type in params_type:
                fp.write(json_default_val[p_type] + '\n')

    
        solution_code = go_generate_solution_code(function_name, params_type, params_name, return_type)
        trailer_code = go_generate_trailer_code(function_name, params_type, params_name, return_type)

        with open(os.path.join(TMP, 'main.go'), 'w') as fp:
            with open(os.path.join(PATH, 'go_header')) as fq:
                fp.write(fq.read() + '\n' + solution_code + trailer_code)
    
        for filename in ['go_parse_tools.go', 'go_io_tools.go', 'go_type_node.go']:
            src = os.path.join(PATH, filename)
            dst = os.path.join(TMP, filename)
            shutil.copy(src, dst)
        
        current_dir = os.getcwd()
    
        os.chdir(TMP)
        result = subprocess.run(['goimports', '-w', 'main.go'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                )

    
        if result.returncode != 0:
            return result.returncode, result.stderr
        
        result = subprocess.run(['go', 'build', '-o', 'main', 'main.go', 'go_io_tools.go', 'go_parse_tools.go', 'go_type_node.go'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                )

    
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
        return 0, {'main_body.go' : solution_code, 'main_trailer.go' : trailer_code}
    finally:
        shutil.rmtree(TMP)

if __name__ == '__main__':
    params_type = [TypeEnum.INT, TypeEnum.LONG, TypeEnum.DOUBLE, TypeEnum.STRING, TypeEnum.INT_LIST,
                   TypeEnum.INT_LIST_LIST, TypeEnum.DOUBLE_LIST, TypeEnum.STRING_LIST, TypeEnum.BOOL_LIST,
                   TypeEnum.BOOL, TypeEnum.TREENODE, TypeEnum.LISTNODE]
    params_name = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']
    return_type = TypeEnum.INT_LIST_LIST
    print(go_test('solve', params_type, params_name, return_type))