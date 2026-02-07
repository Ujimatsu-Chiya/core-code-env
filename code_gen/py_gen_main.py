import os
import shutil
import subprocess
from dataclasses import dataclass
from typing import Dict

from utils import TypeEnum, TypeSpec, MethodDef, json_default_val, ClassDef

PY_TYPE_SPECS: Dict[TypeEnum, TypeSpec] = {
    TypeEnum.BOOL: TypeSpec('bool', 'False', 'des_bool', 'ser_bool'),
    TypeEnum.INT: TypeSpec('int', '0', 'des_int', 'ser_int'),
    TypeEnum.LONG: TypeSpec('int', '0', 'des_long', 'ser_long'),
    TypeEnum.DOUBLE: TypeSpec('float', '0.0', 'des_double', 'ser_double'),
    TypeEnum.STRING: TypeSpec('str', '""', 'des_string', 'ser_string'),
    TypeEnum.INT_LIST: TypeSpec('List[int]', '[]', 'des_int_list', 'ser_int_list'),
    TypeEnum.INT_LIST_LIST: TypeSpec('List[List[int]]', '[]', 'des_int_list_list', 'ser_int_list_list'),
    TypeEnum.DOUBLE_LIST: TypeSpec('List[float]', '[]', 'des_double_list', 'ser_double_list'),
    TypeEnum.STRING_LIST: TypeSpec('List[str]', '[]', 'des_string_list', 'ser_string_list'),
    TypeEnum.BOOL_LIST: TypeSpec('List[bool]', '[]', 'des_bool_list', 'ser_bool_list'),
    TypeEnum.TREENODE: TypeSpec('TreeNode', 'None', 'des_tree', 'ser_tree'),
    TypeEnum.LISTNODE: TypeSpec('ListNode', 'None', 'des_linked_list', 'ser_linked_list'),
    TypeEnum.LONG_LIST: TypeSpec('List[int]', '[]', 'des_long_list', 'ser_long_list'),
    TypeEnum.NONE: TypeSpec('None', 'None', 'des_none', 'ser_none'),
}

TIME_COST_PATH = 'time_cost.txt'

@dataclass
class PyMethodDef(MethodDef):
    def generate(self) -> str:
        params_list = []
        for p_type, p_name in zip(self.params_type, self.params_name):
            p_type_str = PY_TYPE_SPECS[p_type].lang_type
            params_list.append(f'{p_name}: {p_type_str}')
        py_signature = f"def {self.function_name}(self, {', '.join(params_list)}) -> {PY_TYPE_SPECS[self.return_type].lang_type}:"
        return py_signature

@dataclass
class PyClassDef(ClassDef):
    def __post_init__(self):
        self.constructor.function_name = '__init__'
        self.constructor.return_type = TypeEnum.NONE

    def constructor_generate(self):
        return self.constructor.generate()

def py_generate_solution_code(method_def: PyMethodDef) -> str:
    lines = [
        f'class Solution:',
        f"    {method_def.generate()}",
        f'        # write code here',
        f'        return {PY_TYPE_SPECS[return_type].default}',
    ]
    return "\n".join(lines)

def py_generate_system_code(class_def: PyClassDef) -> str:
    lines = [
        f'class {class_def.name}:',
        f'    {class_def.constructor_generate()}',
        f'        # write code here',
        f'        pass',
        f''
    ]
    for method_def in class_def.methods:
        lines += [
            f'    {method_def.generate()}',
            f'        # write code here',
            f'        return {PY_TYPE_SPECS[method_def.return_type].default}',
            f''
        ]
    return "\n".join(lines)


def py_generate_trailer_code(method_def: PyMethodDef):
    params_num = len(method_def.params_name)
    lines_pre = []
    for i, (p_type, p_name) in enumerate(zip(method_def.params_type, method_def.params_name)):
            lines_pre += [
                 'json_str = reader.read_line()',
                 'if json_str == None:',
                 '    break' if i == 0 else f'    raise ValueError("Testcase is missing the required argument: `{p_name}`")',
                 f"p{i} = {PY_TYPE_SPECS[p_type].des_func}(json_str)"
            ]
    lines = [
        f'',
        f'def run():',
        f'    reader = StdinWrapper()',
        f'    writer = StdoutWrapper()',
        f'    total_time = 0',
        f'',
        f'    while True:',
        f'\n'.join([' ' * 8 + s for s in lines_pre]),
        f'',
        f'        start_stamp = time.process_time_ns()',
        f'        result = Solution().{method_def.function_name}({", ".join(f"p{x}" for x in range(params_num))})',
        f'        end_stamp = time.process_time_ns()',
        f'        total_time += end_stamp - start_stamp',
        f'        writer.write_line({PY_TYPE_SPECS[return_type].ser_func}(result))',
        f'    with open("{TIME_COST_PATH}", "w") as fp:',
        '        fp.write(f"{total_time // 1000000}")',
        f'',
        f'if __name__ == "__main__":',
        f'    try:',
        f'        run()',
        f'    except Exception as e:',
        f'        exc_type, exc_value, exc_traceback = sys.exc_info()',
        f'        sys.stdout = sys.stderr',
        f'        traceback.print_tb(exc_traceback)',
        f'        traceback.print_exception(exc_type, exc_value, None)',
        f'        exit(1)',
    ]
    return "\n".join(lines)


def py_test(method_def: PyMethodDef):
    try:
        TMP = 'tmp'
        PATH = 'python3'
        os.makedirs(TMP, exist_ok=True)
        with open(os.path.join(TMP, 'user.in'),'w') as fp:
            for p_type in params_type:
                fp.write(json_default_val[p_type] + '\n')

        solution_code = py_generate_solution_code(method_def)
        trailer_code = py_generate_trailer_code(method_def)

        with open(os.path.join(TMP, 'main.py'), 'w') as fp:
            with open(os.path.join(PATH, 'py_header')) as fq:
                fp.write(fq.read() + '\n' + solution_code + trailer_code)
    
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
        
        return 0, {'main_body.py' : solution_code, 'main_trailer.py' : trailer_code}
    finally:
        shutil.rmtree(TMP)

if __name__ == '__main__':
    params_type = [TypeEnum.INT, TypeEnum.LONG, TypeEnum.DOUBLE, TypeEnum.STRING, TypeEnum.INT_LIST,
                   TypeEnum.INT_LIST_LIST, TypeEnum.DOUBLE_LIST, TypeEnum.STRING_LIST, TypeEnum.BOOL_LIST,
                   TypeEnum.BOOL, TypeEnum.TREENODE, TypeEnum.LISTNODE]
    params_name = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']
    return_type = TypeEnum.INT_LIST_LIST
    # print(py_generate_trailer_code(MethodDef('solve', params_type, params_name, return_type)))
    m1 = PyMethodDef('solve', params_type, params_name, return_type)
    m2 = PyMethodDef('solve2', params_type, params_name, TypeEnum.INT)
    m3 = PyMethodDef('solve2', params_type, params_name, TypeEnum.INT)
    # print(m2)
    print(py_generate_system_code(PyClassDef("System", m3, [m1, m2])))


