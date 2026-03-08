"""Python code generator compatibility entrypoint."""

from utils import TypeEnum
from py_gen_common import PY_TYPE_SPECS, TIME_COST_PATH, PyMethodDef, PyClassDef
from py_gen_functional import py_generate_solution_code, py_generate_trailer_code, py_test
from py_gen_system import py_generate_system_code, py_generate_system_trailer_code, py_system_test

__all__ = [
    "PY_TYPE_SPECS",
    "TIME_COST_PATH",
    "PyMethodDef",
    "PyClassDef",
    "py_generate_solution_code",
    "py_generate_trailer_code",
    "py_generate_system_code",
    "py_generate_system_trailer_code",
    "py_test",
    "py_system_test",
]


if __name__ == "__main__":
    params_type = [
        TypeEnum.INT,
        TypeEnum.LONG,
        TypeEnum.DOUBLE,
        TypeEnum.STRING,
        TypeEnum.INT_LIST,
        TypeEnum.INT_LIST_LIST,
        TypeEnum.DOUBLE_LIST,
        TypeEnum.STRING_LIST,
        TypeEnum.BOOL_LIST,
        TypeEnum.BOOL,
        TypeEnum.TREENODE,
        TypeEnum.LISTNODE,
    ]
    params_name = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l"]
    return_type = TypeEnum.INT_LIST_LIST
    m1 = PyMethodDef("solve", params_type, params_name, return_type)
    print(py_generate_solution_code(m1))
    print(py_test(m1))

    ctor = PyMethodDef("ctor", [TypeEnum.INT], ["capacity"], TypeEnum.NONE)
    m2 = PyMethodDef("put", [TypeEnum.INT, TypeEnum.INT], ["key", "value"], TypeEnum.NONE)
    m3 = PyMethodDef("get", [TypeEnum.INT], ["key"], TypeEnum.INT)
    class_def = PyClassDef("System", ctor, [m2, m3])
    print(py_generate_system_code(class_def))
    print(py_system_test(class_def))
