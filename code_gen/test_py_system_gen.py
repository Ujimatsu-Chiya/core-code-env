import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))

from utils import TypeEnum
from py_gen_common import PyMethodDef, PyClassDef
from py_gen_system import (
    py_generate_system_code,
    py_generate_system_trailer_code,
    py_system_test,
)


class PySystemGenTest(unittest.TestCase):
    def _build_class_def(self) -> PyClassDef:
        ctor = PyMethodDef("ctor", [TypeEnum.INT], ["capacity"], TypeEnum.NONE)
        m1 = PyMethodDef("push", [TypeEnum.INT], ["value"], TypeEnum.NONE)
        m2 = PyMethodDef("peek", [], [], TypeEnum.INT)
        return PyClassDef("CustomStack", ctor, [m1, m2])

    def test_generate_system_templates(self):
        class_def = self._build_class_def()
        body = py_generate_system_code(class_def)
        trailer = py_generate_system_trailer_code(class_def)

        self.assertIn("class CustomStack:", body)
        self.assertIn("def __init__(self, capacity: int) -> None:", body)
        self.assertIn('if methods[0] != "CustomStack":', trailer)
        self.assertIn('if method == "push":', trailer)
        self.assertIn('elif method == "peek":', trailer)

    def test_py_system_test_runs(self):
        class_def = self._build_class_def()
        ret, result = py_system_test(class_def)
        if ret != 0 and isinstance(result, str) and "Python.h: No such file or directory" in result:
            self.skipTest("python3-dev headers are unavailable in current environment")
        self.assertEqual(ret, 0, msg=str(result))
        self.assertIsInstance(result, dict)
        self.assertIn("main_body.py", result)
        self.assertIn("main_trailer.py", result)


if __name__ == "__main__":
    unittest.main()
