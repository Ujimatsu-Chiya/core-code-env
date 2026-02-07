import os
import shutil
import subprocess
from dataclasses import dataclass
from typing import List, Dict
from utils import TypeEnum, json_default_val, TypeSpec, MethodDef, ClassDef

JAVA_TYPE_SPECS: Dict[TypeEnum, TypeSpec] = {
    TypeEnum.BOOL: TypeSpec('boolean', 'false', 'desBool', 'serBool'),
    TypeEnum.INT: TypeSpec('int', '0', 'desInt', 'serInt'),
    TypeEnum.LONG: TypeSpec('long', '0L', 'desLong', 'serLong'),
    TypeEnum.DOUBLE: TypeSpec('double', '0.0', 'desDouble', 'serDouble'),
    TypeEnum.STRING: TypeSpec('String', '""', 'desString', 'serString'),

    TypeEnum.INT_LIST: TypeSpec('int[]', 'null', 'desIntList', 'serIntList'),
    TypeEnum.INT_LIST_LIST: TypeSpec('int[][]', 'null', 'desIntListList', 'serIntListList'),
    TypeEnum.DOUBLE_LIST: TypeSpec('double[]', 'null', 'desDoubleList', 'serDoubleList'),
    TypeEnum.STRING_LIST: TypeSpec('String[]', 'null', 'desStringList', 'serStringList'),
    TypeEnum.BOOL_LIST: TypeSpec('boolean[]', 'null', 'desBoolList', 'serBoolList'),

    TypeEnum.TREENODE: TypeSpec('TreeNode', 'null', 'desTree', 'serTree'),
    TypeEnum.LISTNODE: TypeSpec('ListNode', 'null', 'desLinkedList', 'serLinkedList'),
    TypeEnum.LONG_LIST: TypeSpec('long[]', 'null', 'desLongList', 'serLongList'),
    TypeEnum.NONE: TypeSpec('void', '', 'desNone', 'serNone'),
}

TIME_COST_PATH = 'time_cost.txt'


@dataclass
class JavaMethodDef(MethodDef):
    def generate(self) -> str:
        params_list = []
        for p_type, p_name in zip(self.params_type, self.params_name):
            p_type_str = JAVA_TYPE_SPECS[p_type].lang_type
            params_list.append(f'{p_type_str} {p_name}')
        java_signature = f"public {JAVA_TYPE_SPECS[return_type].lang_type} {self.function_name}({', '.join(params_list)})"
        return java_signature


@dataclass
class JavaClassDef(ClassDef):
    def __post_init__(self):
        self.constructor.function_name = self.name
        self.constructor.return_type = TypeEnum.NONE
    def constructor_generate(self):
        params_list: List[str] = []
        for p_type, p_name in zip(self.constructor.params_type, self.constructor.params_name):
            t = JAVA_TYPE_SPECS[p_type].lang_type
            params_list.append(f"{t} {p_name}")
        signature = f"public {self.name}({', '.join(params_list)})"
        return signature


def java_generate_solution_code(method_def : JavaMethodDef):
    lines = [
        'class Solution{',
        f"    {method_def.generate()}{{",
        '        // write code here',
        f'        return {JAVA_TYPE_SPECS[return_type].default};',
        '    }',
        '}',
        ''
    ]
    return "\n".join(lines)

def java_generate_system_code(class_def: JavaClassDef) -> str:
    lines = [
        f'class {class_def.name}{{',
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
            f'        return {JAVA_TYPE_SPECS[method_def.return_type].default}',
            f'    }}',
            ''
        ]
    lines += [
        f'}}\n'
    ]
    return "\n".join(lines)




def java_generate_trailer_code(method_def : JavaMethodDef):
    params_num = len(params_name)
    lines_pre = []
    for i, (p_type, p_name) in enumerate(zip(method_def.params_type, method_def.params_name)):
            lines_pre += [
                 'jsonStr = reader.readLine();',
                 'if(jsonStr == null){',
                 '    break;' if i == 0 else f'    throw new IllegalArgumentException("Testcase is missing the required argument: `{p_name}`");',
                 '}',
                 f"{JAVA_TYPE_SPECS[p_type].lang_type} p{i} = JavaParseTools.{JAVA_TYPE_SPECS[p_type].des_func}(jsonStr);"
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
        f'            {JAVA_TYPE_SPECS[method_def.return_type].lang_type} result = new Solution().{method_def.function_name}({", ".join(f"p{x}" for x in range(params_num))});',
        '', 
        '            long endStamp = System.nanoTime();', 
        '            totalTime += endStamp - startStamp;', 
        '', 
        f'            writer.writeLine(JavaParseTools.{JAVA_TYPE_SPECS[return_type].ser_func}(result));',
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


def java_test(method_def):
    try:
        TMP = 'tmp'
        PATH = 'java'

        os.makedirs(TMP, exist_ok=True)
        with open(os.path.join(TMP, 'user.in'),'w') as fp:
            for p_type in params_type:
                fp.write(json_default_val[p_type] + '\n')


        solution_code = java_generate_solution_code(method_def)
        trailer_code = java_generate_trailer_code(method_def)

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
    # print(py_generate_trailer_code(MethodDef('solve', params_type, params_name, return_type)))
    m1 = JavaMethodDef('solve', params_type, params_name, return_type)
    m2 = JavaMethodDef('solve2', params_type, params_name, TypeEnum.INT)
    m3 = JavaMethodDef('solve2', params_type, params_name, TypeEnum.INT)
    # print(m2)
    print(java_generate_system_code(JavaClassDef("System", m3, [m1, m2])))


