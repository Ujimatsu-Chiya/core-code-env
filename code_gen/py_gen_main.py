from typing import List
from utils import TypeEnum

py_type = {
    TypeEnum.BOOL: 'bool',
    TypeEnum.INT: 'int',
    TypeEnum.LONG: 'int',
    TypeEnum.DOUBLE: 'float',
    TypeEnum.STRING: 'str',
    TypeEnum.INT_LIST: 'List[int]',
    TypeEnum.INT_LIST_LIST: 'List[List[int]]',
    TypeEnum.DOUBLE_LIST: 'List[float]',
    TypeEnum.STRING_LIST: 'List[str]',
    TypeEnum.BOOL_LIST: 'List[bool]',
    TypeEnum.TREENODE: 'TreeNode',
    TypeEnum.LISTNODE: 'ListNode',
    TypeEnum.LONG_LIST : 'List[int]'
}

py_default_val = {
    TypeEnum.BOOL : 'False',
    TypeEnum.INT : '0',
    TypeEnum.LONG : '0',
    TypeEnum.DOUBLE : '0.0',
    TypeEnum.STRING: '""',
    TypeEnum.INT_LIST: '[]',
    TypeEnum.INT_LIST_LIST: '[]',
    TypeEnum.DOUBLE_LIST: '[]',
    TypeEnum.STRING_LIST: '[]',
    TypeEnum.BOOL_LIST: '[]',
    TypeEnum.TREENODE: 'None',
    TypeEnum.LISTNODE: 'None',
    TypeEnum.LONG_LIST : '[]'
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

def _generate_py_signature(function_name:str, params_type:List[TypeEnum], params_name:List[str], return_type:TypeEnum) -> str:
    params_list = []
    for p_type, p_name in zip(params_type, params_name):
        p_type_str = py_type[p_type]
        params_list.append(f'{p_name}: {p_type_str}')
    py_signature = f"def {function_name}(self, {', '.join(params_list)}) -> {py_type[return_type]}:"
    return py_signature

def py_generate_solution_code(function_name:str, params_type:List[TypeEnum], params_name:List[str], return_type:TypeEnum):
    lines = [
        'class Solution:',
        f"    {_generate_py_signature(function_name, params_type, params_name, return_type)}",
        '        # write code here',
        f'        return {py_default_val[return_type]}',
    ]
    return "\n".join(lines)

def py_generate_main_code(function_name:str, params_type:List[TypeEnum], params_name:List[str], return_type:TypeEnum):
    params_num = len(params_name)
    lines_pre = []
    for i, (p_type, p_name) in enumerate(zip(params_type, params_name)):
            lines_pre += [
                 'json_str = reader.read_line()',
                 'if json_str == None:',
                 '    break' if i == 0 else f'    raise ValueError("Testcase is missing the required argument: `{p_name}`")',
                 f"p{i} = {des_func_name[p_type]}(json_str)"
            ]
    lines = [
        'from py_io_tools import *',
        'from py_parse_tools import *',
        'from py_node_type import *',
        'from solution import *',
        'import time',
        'import sys',
        'import traceback'
        '',
        '',
        'def run():',
        '    reader = StdinWrapper()',
        '    writer = StdoutWrapper()',
        '    total_time = 0',
        '    while True:',
        '',
        '\n'.join([' ' * 8 + s for s in lines_pre]),
        '',
        '        start_stamp = time.process_time_ns()',
        f'        result = Solution().{function_name}({", ".join(f"p{x}" for x in range(params_num))})',
        '        end_stamp = time.process_time_ns()',
        '        total_time += end_stamp - start_stamp',
        f'        writer.write_line({ser_func_name[return_type]}(result))',
        f'    with open("{TIME_COST_PATH}", "w") as fp:',
        '        fp.write(f"{total_time // 1000000}")',
        '',
        'if __name__ == "__main__":',
        '    try:',
        '        run()',
        '    except Exception as e:',
        '        exc_type, exc_value, exc_traceback = sys.exc_info()',
        '        sys.stdout = sys.stderr',
        '        traceback.print_tb(exc_traceback)',
        '        traceback.print_exception(exc_type, exc_value, None)',
        '        exit(1)',
    ]
    return "\n".join(lines)

