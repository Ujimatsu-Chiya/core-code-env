import sys
import sysconfig
from setuptools import setup, Extension

# 获取当前 Python 版本号
python_version = sys.version_info
python_version_str = f"python{python_version.major}.{python_version.minor}"

# 获取 Python 库路径
python_lib_dir = sysconfig.get_paths()["stdlib"]

# 定义扩展模块
module = Extension(
    "py_parse_module",  # 模块名称
    sources=[
        "py_parse_module.cpp",  # Python 接口的实现
        "../rapidjson_helper.cpp"  # RapidJSON 相关逻辑
    ],
    include_dirs=[
        sysconfig.get_paths()["include"],  # 获取 Python 头文件路径
        ".."  # RapidJSON 辅助头文件路径
    ],
    library_dirs=[
        python_lib_dir,  # Python 库路径
        "/usr/lib/x86_64-linux-gnu"  # 系统库路径
    ],
    libraries=[python_version_str],  # 自动设置库名称，类似 "python3.10"
    extra_compile_args=["-std=c++11", "-fPIC"],  # C++ 编译选项
)

# 调用 setup 函数
setup(
    name="py_parse_module",
    version="1.0",
    description="A Python module for parsing JSON arrays using RapidJSON.",
    ext_modules=[module],
)


'''
python3 setup.py build --build-lib .
python3 -m py_compile py_node_type.py py_parse_tools.py
'''