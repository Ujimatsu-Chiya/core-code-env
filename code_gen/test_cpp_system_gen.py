import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))

from utils import TypeEnum
from cpp_gen_common import CppMethodDef, CppClassDef
from cpp_gen_system import (
    cpp_generate_system_code,
    cpp_generate_system_trailer_code,
    cpp_system_test,
)


class CppSystemGenTest(unittest.TestCase):
    def _build_class_def(self) -> CppClassDef:
        ctor = CppMethodDef("ctor", [TypeEnum.INT], ["capacity"], TypeEnum.NONE)
        m1 = CppMethodDef("push", [TypeEnum.INT], ["value"], TypeEnum.NONE)
        m2 = CppMethodDef("peek", [], [], TypeEnum.INT)
        return CppClassDef("CustomStack", ctor, [m1, m2])

    def test_generate_system_templates(self):
        class_def = self._build_class_def()
        body = cpp_generate_system_code(class_def)
        trailer = cpp_generate_system_trailer_code(class_def)

        self.assertIn("class CustomStack{", body)
        self.assertIn("CustomStack(int capacity)", body)
        self.assertIn('if (methods[0] != "CustomStack") {', trailer)
        self.assertIn('if (method == "push") {', trailer)
        self.assertIn('else if (method == "peek") {', trailer)

    def test_cpp_system_test_compiles_and_runs(self):
        class_def = self._build_class_def()
        ret, result = cpp_system_test(class_def)
        self.assertEqual(ret, 0, msg=str(result))
        self.assertIsInstance(result, dict)
        self.assertIn("main_body.cpp", result)
        self.assertIn("main_trailer.cpp", result)


if __name__ == "__main__":
    unittest.main()
