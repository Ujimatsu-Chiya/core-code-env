import os
import sys
import sysconfig
from setuptools import setup, Extension

python_version = sys.version_info
python_version_str = f"python{python_version.major}.{python_version.minor}"
python_lib_dir = sysconfig.get_paths()["stdlib"]

runtime_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.abspath(os.path.join(runtime_dir, "..", ".."))

helper_cpp = os.environ.get(
    "CODE_GEN_RAPIDJSON_HELPER_CPP",
    os.path.join(repo_root, "code_gen", "assets", "rapidjson_helper.cpp"),
)
helper_include_dir = os.environ.get(
    "CODE_GEN_RAPIDJSON_HELPER_INCLUDE_DIR",
    os.path.dirname(helper_cpp),
)

module = Extension(
    "py_parse_module",
    sources=[
        "py_parse_module.cpp",
        helper_cpp,
    ],
    include_dirs=[
        sysconfig.get_paths()["include"],
        helper_include_dir,
    ],
    library_dirs=[
        python_lib_dir,
    ],
    libraries=[python_version_str],
    extra_compile_args=["-std=c++11", "-fPIC"],
)

setup(
    name="py_parse_module",
    version="1.0",
    description="A Python module for parsing JSON arrays using RapidJSON.",
    ext_modules=[module],
)
