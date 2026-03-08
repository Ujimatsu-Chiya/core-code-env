"""C++ code generator compatibility entrypoint."""

from utils import TypeEnum
from cpp_gen_common import CPP_TYPE_SPECS, TIME_COST_PATH, CppMethodDef, CppClassDef
from cpp_gen_functional import cpp_generate_solution_code, cpp_generate_trailer_code, cpp_test
from cpp_gen_system import cpp_generate_system_code, cpp_generate_system_trailer_code, cpp_system_test

__all__ = [
    "CPP_TYPE_SPECS",
    "TIME_COST_PATH",
    "CppMethodDef",
    "CppClassDef",
    "cpp_generate_solution_code",
    "cpp_generate_trailer_code",
    "cpp_generate_system_code",
    "cpp_generate_system_trailer_code",
    "cpp_test",
    "cpp_system_test",
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
    m1 = CppMethodDef("solve", params_type, params_name, return_type)
    print(cpp_generate_solution_code(m1))
    print(cpp_test(m1))

    # System-design example (compatible with the old commented "System" style).
    ctor = CppMethodDef("ctor", [TypeEnum.INT], ["capacity"], TypeEnum.NONE)
    m2 = CppMethodDef("put", [TypeEnum.INT, TypeEnum.INT], ["key", "value"], TypeEnum.NONE)
    m3 = CppMethodDef("get", [TypeEnum.INT], ["key"], TypeEnum.INT)
    class_def = CppClassDef("System", ctor, [m2, m3])
    print(cpp_generate_system_code(class_def))
    print(cpp_system_test(class_def))
