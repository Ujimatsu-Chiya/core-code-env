from setuptools import setup, Extension

# 定义扩展模块
module = Extension(
    "py_parse_tools",  # 模块名称
    sources=[
        "py_parse_tools.cpp",  # Python 接口的实现
        "rapidjson_helper.cpp"  # RapidJSON 相关逻辑
    ],
    include_dirs=[
        "/usr/include/python3.10",  # Python 头文件路径
        "."  # RapidJSON 辅助头文件路径
    ],
    library_dirs=[
        "/usr/lib/python3.10/config-3.10-x86_64-linux-gnu",  # Python 库路径
        "/usr/lib/x86_64-linux-gnu"  # 系统库路径
    ],
    libraries=["python3.10"],  # 需要链接的库
    extra_compile_args=["-std=c++11", "-fPIC"],  # C++ 编译选项
)

# 调用setup函数
setup(
    name="py_parse_tools",
    version="1.0",
    description="A Python module for parsing JSON arrays using RapidJSON.",
    ext_modules=[module],
)