from typing import List
from utils import TypeEnum

java_type = {
    TypeEnum.BOOL: 'boolean',
    TypeEnum.INT: 'int',
    TypeEnum.LONG: 'long',
    TypeEnum.DOUBLE: 'double',
    TypeEnum.STRING: 'String',
    TypeEnum.INT_LIST: 'int[]',
    TypeEnum.INT_LIST_LIST: 'int[][]',
    TypeEnum.DOUBLE_LIST: 'double[]',
    TypeEnum.STRING_LIST: 'String[]',
    TypeEnum.BOOL_LIST: 'boolean[]',
    TypeEnum.TREENODE: 'TreeNode',
    TypeEnum.LISTNODE: 'ListNode',
    TypeEnum.LONG_LIST: 'long[]'
}

java_default_val = {
    TypeEnum.BOOL: 'false',
    TypeEnum.INT: '0',
    TypeEnum.LONG: '0L',
    TypeEnum.DOUBLE: '0.0',
    TypeEnum.STRING: '""',
    TypeEnum.INT_LIST: 'null',
    TypeEnum.INT_LIST_LIST: 'null',
    TypeEnum.DOUBLE_LIST: 'null',
    TypeEnum.STRING_LIST: 'null',
    TypeEnum.BOOL_LIST: 'null',
    TypeEnum.TREENODE: 'null',
    TypeEnum.LISTNODE: 'null',
    TypeEnum.LONG_LIST: 'null'
}


des_func_name = {
    TypeEnum.BOOL : 'desBool',
    TypeEnum.INT : 'desInt',
    TypeEnum.LONG : 'desLong',
    TypeEnum.DOUBLE : 'desDouble',
    TypeEnum.STRING: 'desString',
    TypeEnum.INT_LIST: 'desIntList',
    TypeEnum.INT_LIST_LIST: 'desIntListList',
    TypeEnum.DOUBLE_LIST: 'desDoubleList',
    TypeEnum.STRING_LIST: 'desStringList',
    TypeEnum.BOOL_LIST: 'desBoolList',
    TypeEnum.TREENODE: 'desTree',
    TypeEnum.LISTNODE: 'desLinkedList',
    TypeEnum.LONG_LIST : 'desLongList'
}

ser_func_name = {
    TypeEnum.BOOL : 'serBool',
    TypeEnum.INT : 'serInt',
    TypeEnum.LONG : 'serLong',
    TypeEnum.DOUBLE : 'serDouble',
    TypeEnum.STRING: 'serString',
    TypeEnum.INT_LIST: 'serIntList',
    TypeEnum.INT_LIST_LIST: 'serIntListList',
    TypeEnum.DOUBLE_LIST: 'serDoubleList',
    TypeEnum.STRING_LIST: 'serStringList',
    TypeEnum.BOOL_LIST: 'serBoolList',
    TypeEnum.TREENODE: 'serTree',
    TypeEnum.LISTNODE: 'serLinkedList',
    TypeEnum.LONG_LIST : 'serLongList'
}

TIME_COST_PATH = 'time_cost.txt'

def _generate_java_signature(function_name:str, params_type:List[TypeEnum], params_name:List[str], return_type:TypeEnum) -> str:
    params_list = []
    for p_type, p_name in zip(params_type, params_name):
        p_type_str = java_type[p_type]
        params_list.append(f'{p_type_str} {p_name}')
    java_signature = f"public {java_type[return_type]} {function_name}({', '.join(params_list)})"
    return java_signature



def java_generate_solution_code(function_name:str, params_type:List[TypeEnum], params_name:List[str], return_type:TypeEnum):
    lines = [
        'public class Solution{',
        f"    {_generate_java_signature(function_name, params_type, params_name, return_type)}{{",
        '        // write code here',
        f'        return {java_default_val[return_type]};',
        '    }',
        '}'
    ]
    return "\n".join(lines)




def java_generate_main_code(function_name:str, params_type:List[TypeEnum], params_name:List[str], return_type:TypeEnum):
    params_num = len(params_name)
    lines_pre = []
    for i, (p_type, p_name) in enumerate(zip(params_type, params_name)):
            lines_pre += [
                 'jsonStr = reader.readLine();',
                 'if(jsonStr == null){',
                 '    break;' if i == 0 else f'    throw new IllegalArgumentException("Testcase is missing the required argument: `{p_name}`");',
                 '}',
                 f"{java_type[p_type]} p{i} = JavaParseTools.{des_func_name[p_type]}(jsonStr);"
            ]
    lines = [
        'import java.io.*;', 
        'import java.time.*;', 
        'import java.util.*;', 
        '', 
        'public class Main {', 
        '',
        '    public static void run() throws IOException{', 
        '        StdinWrapper reader = new StdinWrapper();', 
        '        StdoutWrapper writer = new StdoutWrapper();', 
        '        long totalTime = 0;', 
        '        String jsonStr = null;'
        '', 
        '        while (true) {',
        '\n'.join([' ' * 12 + s for s in lines_pre]),
        '            long startStamp = System.nanoTime();', 
        '', 
        f'            {java_type[return_type]} result = new Solution().{function_name}({", ".join(f"p{x}" for x in range(params_num))});',
        '', 
        '            long endStamp = System.nanoTime();', 
        '            totalTime += endStamp - startStamp;', 
        '', 
        f'            writer.writeLine(JavaParseTools.{ser_func_name[return_type]}(result));', 
        '            ', 
        '        }', 
        f'        try (BufferedWriter fp = new BufferedWriter(new FileWriter("{TIME_COST_PATH}"))) {{', 
        '            fp.write(String.format("%d", totalTime / 1000000));', 
        '        } catch (IOException e) {', 
        '            e.printStackTrace();', 
        '        }', 
        '    }', 
        '', 
        '    public static void main(String[] args) {', 
        '        try {', 
        '            run();', 
        '        } catch (Exception e) {',
        '            e.printStackTrace();', 
        '            System.exit(1);', 
        '        }', 
        '    }', 
        '}'
        ]
    return "\n".join(lines)

if __name__ == '__main__':
    params_type = [TypeEnum.INT, TypeEnum.LONG, TypeEnum.DOUBLE, TypeEnum.STRING, TypeEnum.INT_LIST,
                   TypeEnum.INT_LIST_LIST, TypeEnum.DOUBLE_LIST, TypeEnum.STRING_LIST, TypeEnum.BOOL_LIST,
                   TypeEnum.BOOL, TypeEnum.TREENODE, TypeEnum.LISTNODE][:4]
    params_name = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l'][:4]
    return_type = TypeEnum.INT_LIST_LIST
    print(java_generate_main_code('solve', params_type, params_name, return_type))
