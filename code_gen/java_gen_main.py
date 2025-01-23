import os
import shutil
import subprocess
from typing import List
from utils import TypeEnum, json_default_val

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

def _java_generate_signature(function_name:str, params_type:List[TypeEnum], params_name:List[str], return_type:TypeEnum) -> str:
    params_list = []
    for p_type, p_name in zip(params_type, params_name):
        p_type_str = java_type[p_type]
        params_list.append(f'{p_type_str} {p_name}')
    java_signature = f"public {java_type[return_type]} {function_name}({', '.join(params_list)})"
    return java_signature



def java_generate_solution_code(function_name:str, params_type:List[TypeEnum], params_name:List[str], return_type:TypeEnum):
    lines = [
        'class Solution{',
        f"    {_java_generate_signature(function_name, params_type, params_name, return_type)}{{",
        '        // write code here',
        f'        return {java_default_val[return_type]};',
        '    }',
        '}',
        ''
    ]
    return "\n".join(lines)




def java_generate_trailer_code(function_name:str, params_type:List[TypeEnum], params_name:List[str], return_type:TypeEnum):
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


def java_test(function_name:str, params_type:List[TypeEnum], params_name:List[str], return_type:TypeEnum):
    try:
        TMP = 'tmp'
        PATH = 'java'

        os.makedirs(TMP, exist_ok=True)
        with open(os.path.join(TMP, 'user.in'),'w') as fp:
            for p_type in params_type:
                fp.write(json_default_val[p_type] + '\n')


        solution_code = java_generate_solution_code(function_name, params_type, params_name, return_type)
        trailer_code = java_generate_trailer_code(function_name, params_type, params_name, return_type)

        with open(os.path.join(TMP, 'Main.java'), 'w') as fp:
            with open(os.path.join(PATH, 'java_header')) as fq:
                fp.write(fq.read() + '\n' + solution_code + trailer_code)
    
        tmp_list = [filename for filename in os.listdir(PATH) if filename.startswith('libjava_') and filename.endswith('.so')]
        current_dir = os.getcwd()
        if len(tmp_list) == 0:
            print(f"No files matching the condition were found in the {PATH} directory. Running the build command...")
            os.chdir(PATH)
            subprocess.run(
                'g++ -fPIC -shared -o libjava_parse_module.so java_parse_module.cpp ../rapidjson_helper.cpp -I$JAVA_HOME/include -I$JAVA_HOME/include/linux',
                shell=True
            )
            os.chdir(current_dir)
        else:
            print(f"{tmp_list[0]} already exists in the {PATH} directory. No need to run the build command.")

        for filename in ['JavaIoTools.java', 'JavaNodeType.java', 'JavaParseModule.h', 'JavaParseModule.java', 'JavaParseModule.java', 'JavaParseTools.java', 'libjava_parse_module.so']:
            src = os.path.join(PATH, filename)
            dst = os.path.join(TMP, filename)
            shutil.copy(src, dst)
    
        os.chdir(TMP)
        result = subprocess.run('javac *.java',
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True)

    
        if result.returncode != 0:
            return result.returncode, result.stderr
    
        result = subprocess.run(['java', '-Djava.library.path=.', 'Main'],
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
        return 0, {'MainBody.java' : solution_code, 'MainTrailer.java' : trailer_code}
    finally:
        shutil.rmtree(TMP)

if __name__ == '__main__':
    params_type = [TypeEnum.INT, TypeEnum.LONG, TypeEnum.DOUBLE, TypeEnum.STRING, TypeEnum.INT_LIST,
                   TypeEnum.INT_LIST_LIST, TypeEnum.DOUBLE_LIST, TypeEnum.STRING_LIST, TypeEnum.BOOL_LIST,
                   TypeEnum.BOOL, TypeEnum.TREENODE, TypeEnum.LISTNODE]
    params_name = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']
    return_type = TypeEnum.INT_LIST_LIST
    print(java_test('solve', params_type, params_name, return_type))