import shutil
import subprocess
from typing import List
from utils import *
from py_gen_main import py_generate_main_code, py_generate_solution_code
from cpp_gen_main import cpp_generate_trailer_code, cpp_generate_solution_code
from java_gen_main import java_generate_main_code, java_generate_solution_code
import os

json_default_val = {
    TypeEnum.BOOL : 'false',
    TypeEnum.INT : '0',
    TypeEnum.LONG : '0',
    TypeEnum.DOUBLE : '0.0',
    TypeEnum.STRING: '"a"',
    TypeEnum.INT_LIST: '[1]',
    TypeEnum.INT_LIST_LIST: '[[1]]',
    TypeEnum.DOUBLE_LIST: '[1.0]',
    TypeEnum.STRING_LIST: '["a"]',
    TypeEnum.BOOL_LIST: '[false, true]',
    TypeEnum.TREENODE: '[1,null,2]',
    TypeEnum.LISTNODE: '[1,2]',
    TypeEnum.LONG_LIST : '[1]'
}

TMP = 'tmp'

def test_py(function_name:str, params_type:List[TypeEnum], params_name:List[str], return_type:TypeEnum):
    try:
        os.makedirs(TMP, exist_ok=True)
        with open(os.path.join(TMP, 'user.in'),'w') as fp:
            for p_type in params_type:
                fp.write(json_default_val[p_type] + '\n')

        PATH = 'python3'
    
        solution_code = py_generate_solution_code(function_name, params_type, params_name, return_type)

        with open(os.path.join(TMP, 'solution.py'), 'w') as fp:
            with open(os.path.join(PATH, 'py_header')) as fq:
                fp.write(fq.read() + '\n' + solution_code)
    
        tmp_list = [filename for filename in os.listdir(PATH) if filename.startswith('py') and filename.endswith('.so')]
        current_dir = os.getcwd()
        if len(tmp_list) == 0:
            print(f"No files matching the condition were found in the {PATH} directory. Running the build command...")
            os.chdir(PATH)
            subprocess.run(['python3', 'setup.py', 'build', '--build-lib', '.'])
            os.chdir(current_dir)
        else:
            print(f"{tmp_list[0]} already exists in the {PATH} directory. No need to run the build command.")

        for filename in os.listdir(PATH):
            if filename.startswith('py') and (filename.endswith('.py') or filename.endswith('.so')):
                src = os.path.join(PATH, filename)
                dst = os.path.join(TMP, filename)
                shutil.copy(src, dst)
    
        main_code = py_generate_main_code(function_name, params_type, params_name, return_type)
        with open(os.path.join(TMP, 'main.py'), 'w') as fp:
            fp.write(main_code)
    
        os.chdir(TMP)
        result = subprocess.run(['python3', 'main.py'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)

        os.chdir(current_dir)
        if result.returncode != 0:
           return result.returncode, result.stderr

        required_files = ['user.out', 'time_cost.txt']
        files_in_directory = os.listdir(TMP)

        missing_files = [file for file in required_files if file not in files_in_directory]
        if missing_files:
            return 1, f"Missing these files: {', '.join(missing_files)}"
        
        return 0, 'OK'
    finally:
        shutil.rmtree(TMP)
    
def test_cpp(function_name:str, params_type:List[TypeEnum], params_name:List[str], return_type:TypeEnum):
    try:
        os.makedirs(TMP, exist_ok=True)
        with open(os.path.join(TMP, 'user.in'),'w') as fp:
            for p_type in params_type:
                fp.write(json_default_val[p_type] + '\n')

        PATH = 'cpp'
    
        solution_code = cpp_generate_solution_code(function_name, params_type, params_name, return_type)
        trailer_code = cpp_generate_trailer_code(function_name, params_type, params_name, return_type)

        with open(os.path.join(TMP, 'main.cpp'), 'w') as fp:
            with open(os.path.join(PATH, 'cpp_header')) as fq:
                fp.write(fq.read() + '\n' + solution_code + trailer_code)
    
        tmp_list = [filename for filename in os.listdir(PATH) if filename.startswith('libcpp') and filename.endswith('.so')]
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
        return 0, 'OK'
    finally:
        shutil.rmtree(TMP)
        pass
    
def test_java(function_name:str, params_type:List[TypeEnum], params_name:List[str], return_type:TypeEnum):
    try:
        os.makedirs(TMP, exist_ok=True)
        with open(os.path.join(TMP, 'user.in'),'w') as fp:
            for p_type in params_type:
                fp.write(json_default_val[p_type] + '\n')

        PATH = 'java'
    
        solution_code = java_generate_solution_code(function_name, params_type, params_name, return_type)
        main_code = java_generate_main_code(function_name, params_type, params_name, return_type)

        with open(os.path.join(TMP, 'Main.java'), 'w') as fp:
            fp.write(main_code)
        
        with open(os.path.join(TMP, 'Solution.java'), 'w') as fp:
            fp.write(solution_code)
    
        tmp_list = [filename for filename in os.listdir(PATH) if filename.startswith('libjava') and filename.endswith('.so')]
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
        return 0, 'OK'
    finally:
        shutil.rmtree(TMP)
        pass


def test(function_name:str, params_type:List[TypeEnum], params_name:List[str], return_type:TypeEnum):
    assert len(params_name) == len(params_type)
    RESULT = 'result'
    os.makedirs(RESULT, exist_ok=True)
    function_name = to_snake_case(function_name)
    params_name = list(map(to_snake_case, params_name))
    ok, msg = test_py(function_name, params_type, params_name, return_type)
    if ok == 0:
        solution_code = py_generate_solution_code(function_name, params_type, params_name, return_type)
        main_code = py_generate_main_code(function_name, params_type, params_name, return_type)
        with open(os.path.join(RESULT, 'solution.py'), 'w') as fp:
            fp.write(solution_code)
        with open(os.path.join(RESULT, 'main.py'), 'w') as fp:
            fp.write(main_code)
    else:
        print(msg)


if __name__ == '__main__':
    params_type = [TypeEnum.INT, TypeEnum.LONG, TypeEnum.DOUBLE, TypeEnum.STRING, TypeEnum.INT_LIST,
                   TypeEnum.INT_LIST_LIST, TypeEnum.DOUBLE_LIST, TypeEnum.STRING_LIST, TypeEnum.BOOL_LIST,
                   TypeEnum.BOOL, TypeEnum.TREENODE, TypeEnum.LISTNODE][:1]
    params_name = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l'][:1]
    return_type = TypeEnum.INT_LIST_LIST
    print(test_java('solve', params_type, params_name, return_type))