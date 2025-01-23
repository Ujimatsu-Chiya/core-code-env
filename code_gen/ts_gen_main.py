import os
import shutil
import subprocess
from typing import List
from utils import TypeEnum, json_default_val

ts_type = {
    TypeEnum.BOOL: 'boolean',
    TypeEnum.INT: 'number',
    TypeEnum.LONG: 'number',
    TypeEnum.DOUBLE: 'number',
    TypeEnum.STRING: 'string',
    TypeEnum.INT_LIST: 'number[]',
    TypeEnum.INT_LIST_LIST: 'number[][]',
    TypeEnum.DOUBLE_LIST: 'number[]',
    TypeEnum.STRING_LIST: 'string[]',
    TypeEnum.BOOL_LIST: 'boolean[]',
    TypeEnum.TREENODE: 'TreeNode | null',
    TypeEnum.LISTNODE: 'ListNode | null',
    TypeEnum.LONG_LIST: 'number[]'
}

ts_default_val = {
    TypeEnum.BOOL: 'false',
    TypeEnum.INT: '0',
    TypeEnum.LONG: '0',
    TypeEnum.DOUBLE: '0.0',
    TypeEnum.STRING: '""',
    TypeEnum.INT_LIST: '[]',
    TypeEnum.INT_LIST_LIST: '[]',
    TypeEnum.DOUBLE_LIST: '[]',
    TypeEnum.STRING_LIST: '[]',
    TypeEnum.BOOL_LIST: '[]',
    TypeEnum.TREENODE: 'null',
    TypeEnum.LISTNODE: 'null',
    TypeEnum.LONG_LIST: '[]'
}

des_func_name = {
    TypeEnum.BOOL : 'desBool',
    TypeEnum.INT : 'desNumber',
    TypeEnum.LONG : 'desNumber',
    TypeEnum.DOUBLE : 'desNumber',
    TypeEnum.STRING: 'desString',
    TypeEnum.INT_LIST: 'desNumberList',
    TypeEnum.INT_LIST_LIST: 'desNumberListList',
    TypeEnum.DOUBLE_LIST: 'desNumberList',
    TypeEnum.STRING_LIST: 'desStringList',
    TypeEnum.BOOL_LIST: 'desBoolList',
    TypeEnum.TREENODE: 'desTree',
    TypeEnum.LISTNODE: 'desLinkedList',
    TypeEnum.LONG_LIST : 'desNumberList'
}

ser_func_name = {
    TypeEnum.BOOL : 'serBool',
    TypeEnum.INT : 'serNumber',
    TypeEnum.LONG : 'serNumber',
    TypeEnum.DOUBLE : 'serNumber',
    TypeEnum.STRING: 'serString',
    TypeEnum.INT_LIST: 'serNumberList',
    TypeEnum.INT_LIST_LIST: 'serNumberListList',
    TypeEnum.DOUBLE_LIST: 'serNumberList',
    TypeEnum.STRING_LIST: 'serStringList',
    TypeEnum.BOOL_LIST: 'serBoolList',
    TypeEnum.TREENODE: 'serTree',
    TypeEnum.LISTNODE: 'serLinkedList',
    TypeEnum.LONG_LIST : 'serNumberList'
}

TIME_COST_PATH = 'time_cost.txt'

def _ts_generate_signature(function_name:str, params_type:List[TypeEnum], params_name:List[str], return_type:TypeEnum) -> str:
    params_list = []
    for p_type, p_name in zip(params_type, params_name):
        p_type_str = ts_type[p_type]
        params_list.append(f'{p_name}: {p_type_str}')
    ts_signature = f"{function_name}({', '.join(params_list)}) : {ts_type[return_type]}"
    return ts_signature

def ts_generate_solution_code(function_name:str, params_type:List[TypeEnum], params_name:List[str], return_type:TypeEnum):
    lines = [
        f'function {_ts_generate_signature(function_name, params_type, params_name, return_type)}{{',
        '    // write code here',
        f'    return {ts_default_val[return_type]};',
        '}',
    ]
    return "\n".join(lines)

def ts_generate_trailer_code(function_name:str, params_type:List[TypeEnum], params_name:List[str], return_type:TypeEnum):
    params_num = len(params_name)
    lines_pre = []
    for i, (p_type, p_name) in enumerate(zip(params_type, params_name)):
        lines_pre += [
            'jsonStr = reader.readLine();',
            'if (jsonStr === null) {',
            '    break;' if i == 0 else f'    throw new Error("Testcase is missing the required argument: `{p_name}`");',
            '}',
            f'let p{i}: {ts_type[p_type]} = TsParseTools.{des_func_name[p_type]}(jsonStr);'
        ]
    lines = [
        '',
        '',
        'function run() {',
        '    let reader: StdinWrapper = new StdinWrapper();',
        '    let writer: StdoutWrapper = new StdoutWrapper();',
        '    let jsonStr : string | null = null;',
        '    let totalTime = 0;',
        '    while (true) {',
        '',
        '\n'.join([' ' * 8 + s for s in lines_pre]),
        '',
        '        const start = process.hrtime();',
        f'        let result: {ts_type[return_type]} = {function_name}({", ".join(f"p{x}" for x in range(params_num))});',
        '        const end = process.hrtime();',
        '        let startStamp = start[0] * 100000000 + start[1];',
        '        let endStamp = end[0] * 100000000 + end[1];',
        '        totalTime += (endStamp - startStamp);',
        f'        let resultStr: string = TsParseTools.{ser_func_name[return_type]}(result);',
        '        writer.writeLine(resultStr);',
        '    }',
        '    ',
        f"    let fp = fs.createWriteStream(\"{TIME_COST_PATH}\", {{ flags: 'w' }});",
        f'    fp.write(Math.floor(totalTime / 1000000).toString());',
        '}',
        '',
        'run()',
        ''
    ]

    return '\n'.join(lines)


def ts_test(function_name:str, params_type:List[TypeEnum], params_name:List[str], return_type:TypeEnum):
    try:
        TMP = 'tmp'
        PATH = 'typescript'

        os.makedirs(TMP, exist_ok=True)
        with open(os.path.join(TMP, 'user.in'),'w') as fp:
            for p_type in params_type:
                fp.write(json_default_val[p_type] + '\n')

        
    
        solution_code = ts_generate_solution_code(function_name, params_type, params_name, return_type)
        trailer_code = ts_generate_trailer_code(function_name, params_type, params_name, return_type)

        with open(os.path.join(TMP, 'main.ts'), 'w') as fp:
            with open(os.path.join(PATH, 'ts_header')) as fq:
                fp.write(fq.read() + '\n' + solution_code + trailer_code)
    

        current_dir = os.getcwd()

        for filename in ['ts_io_tools.ts', 'ts_parse_tools.ts', 'ts_type_node.ts']:
            src = os.path.join(PATH, filename)
            dst = os.path.join(TMP, filename)
            shutil.copy(src, dst)
    
        os.chdir(TMP)
        result = subprocess.run(['tsc', '--target', 'es6', '--module', 'commonjs', 'main.ts'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)

        if result.returncode != 0:
            return result.returncode, result.stderr
    
        result = subprocess.run(['node', 'main.js'],
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
        return 0, {'main_body.ts' : solution_code, 'main_trailer.ts' : trailer_code}
    finally:
        shutil.rmtree(TMP)

if __name__ == '__main__':
    params_type = [TypeEnum.INT, TypeEnum.LONG, TypeEnum.DOUBLE, TypeEnum.STRING, TypeEnum.INT_LIST,
                   TypeEnum.INT_LIST_LIST, TypeEnum.DOUBLE_LIST, TypeEnum.STRING_LIST, TypeEnum.BOOL_LIST,
                   TypeEnum.BOOL, TypeEnum.TREENODE, TypeEnum.LISTNODE]
    params_name = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']
    return_type = TypeEnum.INT_LIST_LIST
    print(ts_test('solve', params_type, params_name, return_type))