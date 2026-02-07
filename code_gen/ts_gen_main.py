import os
import shutil
import subprocess
from dataclasses import dataclass
from typing import List, Dict
from utils import TypeEnum, json_default_val, TypeSpec, MethodDef

# TypeScript type mapping using unified TypeSpec style
TS_TYPE_SPECS: Dict[TypeEnum, TypeSpec] = {
    TypeEnum.BOOL: TypeSpec('boolean', 'false', 'desBool', 'serBool'),
    TypeEnum.INT: TypeSpec('number', '0', 'desNumber', 'serNumber'),
    TypeEnum.LONG: TypeSpec('number', '0', 'desNumber', 'serNumber'),
    TypeEnum.DOUBLE: TypeSpec('number', '0.0', 'desNumber', 'serNumber'),
    TypeEnum.STRING: TypeSpec('string', '""', 'desString', 'serString'),

    TypeEnum.INT_LIST: TypeSpec('number[]', '[]', 'desNumberList', 'serNumberList'),
    TypeEnum.INT_LIST_LIST: TypeSpec('number[][]', '[]', 'desNumberListList', 'serNumberListList'),
    TypeEnum.DOUBLE_LIST: TypeSpec('number[]', '[]', 'desNumberList', 'serNumberList'),
    TypeEnum.STRING_LIST: TypeSpec('string[]', '[]', 'desStringList', 'serStringList'),
    TypeEnum.BOOL_LIST: TypeSpec('boolean[]', '[]', 'desBoolList', 'serBoolList'),

    TypeEnum.TREENODE: TypeSpec('TreeNode | null', 'null', 'desTree', 'serTree'),
    TypeEnum.LISTNODE: TypeSpec('ListNode | null', 'null', 'desLinkedList', 'serLinkedList'),
    TypeEnum.LONG_LIST: TypeSpec('number[]', '[]', 'desNumberList', 'serNumberList'),

    TypeEnum.NONE: TypeSpec('null', 'null', 'desNone', 'serNone'),
}

TIME_COST_PATH = 'time_cost.txt'


@dataclass
class TsMethodDef(MethodDef):
    """
    Generate TypeScript method signature.
    Example:
        add(a: number, b: number): number
    """

    def generate(self) -> str:
        params_list = []
        for p_type, p_name in zip(self.params_type, self.params_name):
            p_type_str = TS_TYPE_SPECS[p_type].lang_type
            params_list.append(f'{p_name}: {p_type_str}')
        ts_signature = f"{self.function_name}({', '.join(params_list)}) : {TS_TYPE_SPECS[return_type].lang_type}"
        return ts_signature


def ts_generate_solution_code(method: TsMethodDef) -> str:
    lines = [
        "class Solution {",
        f"    {method.generate()} {{",
        "        // write code here",
        f"        return {TS_TYPE_SPECS[method.return_type].lang_type};",
        "    }",
        "}",
    ]
    return "\n".join(lines)


def ts_generate_trailer_code(method: TsMethodDef) -> str:
    params_num = len(params_name)
    lines_pre = []
    for i, (p_type, p_name) in enumerate(zip(method.params_type, method.params_name)):
        lines_pre += [
            'jsonStr = reader.readLine();',
            'if (jsonStr === null) {',
            '    break;' if i == 0 else f'    throw new Error("Testcase is missing the required argument: `{p_name}`");',
            '}',
            f'let p{i}: {TS_TYPE_SPECS[p_type].lang_type} = TsParseTools.{TS_TYPE_SPECS[p_type].des_func}(jsonStr);'
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
        '        let sol = new Solution();',
        f'        let result: {TS_TYPE_SPECS[method.return_type].lang_type} = sol.{method.function_name}({", ".join(f"p{x}" for x in range(params_num))});',
        '        const end = process.hrtime();',
        '        let startStamp = start[0] * 100000000 + start[1];',
        '        let endStamp = end[0] * 100000000 + end[1];',
        '        totalTime += (endStamp - startStamp);',
        f'        let resultStr: string = TsParseTools.{TS_TYPE_SPECS[return_type].ser_func}(result);',
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


def ts_test(method: TsMethodDef) -> str:
    try:
        TMP = 'tmp'
        PATH = 'typescript'

        os.makedirs(TMP, exist_ok=True)
        with open(os.path.join(TMP, 'user.in'), 'w') as fp:
            for p_type in params_type:
                fp.write(json_default_val[p_type] + '\n')

        solution_code = ts_generate_solution_code(method)
        trailer_code = ts_generate_trailer_code(method)

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
        return 0, {'main_body.ts': solution_code, 'main_trailer.ts': trailer_code}
    finally:
        shutil.rmtree(TMP)


if __name__ == '__main__':
    params_type = [TypeEnum.INT, TypeEnum.LONG, TypeEnum.DOUBLE, TypeEnum.STRING, TypeEnum.INT_LIST,
                   TypeEnum.INT_LIST_LIST, TypeEnum.DOUBLE_LIST, TypeEnum.STRING_LIST, TypeEnum.BOOL_LIST,
                   TypeEnum.BOOL, TypeEnum.TREENODE, TypeEnum.LISTNODE]
    params_name = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']
    return_type = TypeEnum.INT_LIST_LIST
    print(ts_generate_solution_code(TsMethodDef('solve', params_type, params_name, return_type)))
    print(ts_generate_trailer_code(TsMethodDef('solve', params_type, params_name, return_type)))