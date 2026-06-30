# core-code-env

`core-code-env` 是一个多语言代码模板生成与运行时验证库，主要面向 LeetCode 风格的
“核心代码模式”题目。

它负责两件事：

- 根据题目签名生成各语言的用户代码模板，也就是 `main_body.<lang>`。
- 生成对应的判题入口/调用逻辑，也就是 `main_trailer.<lang>`，并在本地用 runtime 做一次编译运行验证。

支持两类题型：

- `solution`：普通函数题，只有一个函数入口。
- `system`：系统设计题，包含构造函数和一组方法调用。

当前支持语言：

- C
- C++
- Java
- Python
- TypeScript
- JavaScript
- Go

## 项目结构

```text
.
├── code_gen/                  # Python 生成器
│   ├── core/                  # 编排、类型、路径解析、临时工作区
│   ├── languages/<lang>/      # 各语言生成器
│   ├── cli/                   # CLI 入口
│   ├── assets/                # 打包进 Python 包的公共 C++ helper
│   └── test_and_save.py       # 本地入口
├── runtimes/<lang>/           # 公共 runtime、parser、IO helper
├── scripts/                   # 安装与部署辅助脚本
├── nix/                       # core-code-env runtime 的 Nix derivation
├── result/                    # 示例生成结果
└── gen.sh                     # 生成示例模板
```

## 快速开始

### 安装开发依赖

Ubuntu / Debian 环境可以直接运行：

```bash
bash scripts/setup_dev_env.sh
```

它会依次安装：

- C/C++：`build-essential`、`pkg-config`、`libglib2.0-dev`、`uthash-dev`
- Python：`python3`、`python3-dev`、`pip`、`venv`
- Java：OpenJDK 21
- Go：`golang-go`、`goimports`
- Node/TypeScript：`nodejs`、`npm`、`typescript`、`@types/node`

也可以按语言单独运行：

```bash
bash scripts/setup_gpp.sh
bash scripts/setup_python.sh
bash scripts/setup_java.sh
bash scripts/setup_go.sh
bash scripts/setup_goimports.sh
bash scripts/setup_node_ts.sh
```

### 安装为 Python 包

开发模式：

```bash
python3 -m pip install -e .
```

普通安装：

```bash
python3 -m pip install .
```

安装后可以使用 CLI：

```bash
core-code-env-generate
core-code-env-generate-fast
```

在源码目录中也可以直接运行：

```bash
python3 -m code_gen.cli.test_and_save
python3 -m code_gen.cli.generate_fast
python3 code_gen/test_and_save.py
python3 code_gen/generate_fast.py
./gen.sh
./gen_fast.sh
```

生成结果会写到：

```text
result/solution/main_body.<lang>
result/solution/main_trailer.<lang>
result/system/main_body.<lang>
result/system/main_trailer.<lang>
```

`core-code-env-generate` / `test_and_save.py` 会生成、编译并运行一轮验证。

`core-code-env-generate-fast` / `generate_fast.py` 只生成文件，不编译、不运行，适合批量生成模板或在依赖环境尚未装齐时使用。

## 模板怎么用

生成结果分成两部分：

- `main_body.<lang>`：给用户看的代码模板，通常放进题目的提交区域。
- `main_trailer.<lang>`：平台隐藏的判题入口，用来读入测试数据、调用用户代码、写出结果。

公共 runtime 不应该放进每道题的 `additional_file`。它应该提前安装到沙箱/rootfs 中，例如：

```text
/share/core-code-env/runtimes/
/include/core-code-env/
/lib/libc_parse_tools.so
/lib/libcpp_parse_tools.so
```

判题时，编译脚本会把语言 header、用户代码和 trailer 拼成真正可执行文件。

### 文件名对应关系

| 语言 | 用户模板 | 判题 trailer | OJ 提交文件名 |
| --- | --- | --- | --- |
| C | `main_body.c` | `main_trailer.c` | `foo.c` |
| C++ | `main_body.cpp` | `main_trailer.cpp` | `foo.cc` |
| Java | `main_body.java` | `main_trailer.java` | `Main.java` |
| Python | `main_body.py` | `main_trailer.py` | `foo.py` |
| JavaScript | `main_body.js` | `main_trailer.js` | `foo.js` |
| TypeScript | `main_body.ts` | `main_trailer.ts` | `foo.ts` |
| Go | `main_body.go` | `main_trailer.go` | `foo.go` |

### 在 HydroOJ / 沙箱中编译

仓库提供了 [scripts/core_code_compile.sh](scripts/core_code_compile.sh)，用于在沙箱里拼接并编译核心代码。

它依赖：

- `HYDRO_LANG`：当前语言，例如 `core.c`、`core.cc17`、`core.py3`、`core.java`、`core.ts`。
- `CORE_CODE_RUNTIME_ROOT` 或 `CODE_GEN_RUNTIME_ROOT`：runtime 根目录，默认 `/share/core-code-env/runtimes`。
- `CORE_CODE_INCLUDE_ROOT`：公共 include 根目录，默认 `/include/core-code-env`。
- `CORE_CODE_LIB_DIR`：公共动态库目录，默认 `/lib`。

示例：

```bash
export HYDRO_LANG=core.cc17
export CORE_CODE_RUNTIME_ROOT=/share/core-code-env/runtimes
export CORE_CODE_INCLUDE_ROOT=/include/core-code-env
export CORE_CODE_LIB_DIR=/lib

# 当前目录中应已有 foo.cc 和 main_trailer.cpp
bash /share/core-code-env/core_code_compile.sh
```

编译脚本会按语言生成最终入口：

- C：`c_header + foo.c + main_trailer.c -> main.c -> foo`
- C++：`cpp_header + foo.cc + main_trailer.cpp -> main.cc -> foo`
- Java：`java_header + Solution.java + main_trailer.java -> Main.java -> Main.jar`
- Python：`py_header + foo.py + main_trailer.py -> foo`
- JS/TS/Go：生成对应可执行入口或 JS 输出。

## 用 Python API 生成模板

API 分为两组：

- `generate_solution` / `generate_system`：只生成文件，不验证，速度最快。
- `test_solution` / `test_system`：生成后会编译运行一次，适合开发 generator 或改 runtime 后做检查。

### 普通函数题

```python
from code_gen.core.orchestrator import generate_solution
from code_gen.utils import TypeEnum

result = generate_solution(
    function_name="twoSum",
    params_type=[TypeEnum.INT_LIST, TypeEnum.INT],
    params_name=["nums", "target"],
    return_type=TypeEnum.INT_LIST,
    result_dir="result/two_sum",
)

print(result)
```

如果需要生成后立刻编译运行验证，把 `generate_solution` 换成 `test_solution` 即可。

生成器会根据不同语言自动转换命名风格：

- C / C++ / Python 使用 `snake_case`
- Java / JS / TS 使用 `camelCase`
- Go 函数名使用 `PascalCase`

### 系统设计题

```python
from code_gen.core.orchestrator import generate_system
from code_gen.utils import MethodDef, TypeEnum

result = generate_system(
    class_name="MinStack",
    constructor_params_type=[],
    constructor_params_name=[],
    methods=[
        MethodDef("push", [TypeEnum.INT], ["val"], TypeEnum.NONE),
        MethodDef("pop", [], [], TypeEnum.NONE),
        MethodDef("top", [], [], TypeEnum.INT),
        MethodDef("getMin", [], [], TypeEnum.INT),
    ],
    result_dir="result/min_stack",
)

print(result)
```

如果需要验证系统设计题模板，把 `generate_system` 换成 `test_system`。

### 支持的类型

| TypeEnum | 含义 |
| --- | --- |
| `BOOL` | 布尔 |
| `INT` | 整数 |
| `LONG` | 长整数 |
| `DOUBLE` | 浮点数 |
| `STRING` | 字符串 |
| `INT_LIST` | 整数数组 |
| `LONG_LIST` | 长整数数组 |
| `DOUBLE_LIST` | 浮点数组 |
| `STRING_LIST` | 字符串数组 |
| `BOOL_LIST` | 布尔数组 |
| `INT_LIST_LIST` | 二维整数数组 |
| `TREENODE` | 二叉树 |
| `LISTNODE` | 链表 |
| `NONE` | 无返回值 |

## Runtime 路径解析

运行时目录由 [code_gen/core/runtime_layout.py](code_gen/core/runtime_layout.py) 解析，优先级：

1. `CODE_GEN_RUNTIME_<LANG>_PATH`
2. `CODE_GEN_RUNTIME_ROOT/<lang>`
3. `CODE_GEN_CORE_ROOT/runtimes/<lang>`
4. Python 包资源 `runtimes/<lang>`
5. 源码目录 `runtimes/<lang>`

示例：

```bash
export CODE_GEN_RUNTIME_ROOT=/abs/path/to/runtimes
export CODE_GEN_CORE_ROOT=/abs/path/to/core-code-env-runtime
export CODE_GEN_RUNTIME_CPP_PATH=/abs/path/to/custom/cpp_runtime
```

C/C++/Java/Python parser 共用的 `rapidjson_helper.cpp` 和 `rapidjson_helper.h`
以 `code_gen/assets/` 作为源码中的唯一副本。默认会从 Python 包资源或安装后的
`CODE_GEN_CORE_ROOT` 中解析，也可以手动覆盖：

```bash
export CODE_GEN_RAPIDJSON_HELPER_CPP=/abs/path/to/rapidjson_helper.cpp
export CODE_GEN_RAPIDJSON_HELPER_INCLUDE_DIR=/abs/path/to/include-dir
```

临时目录默认在 `.tmp/` 下，可以覆盖：

```bash
export CODE_GEN_TMP_ROOT=/abs/path/to/tmp_root
```

## 安装 runtime 到沙箱

### 非 Nix 环境

```bash
bash scripts/install_runtime.sh /usr/local
```

安装后布局：

```text
/usr/local/share/core-code-env/
  runtimes/
  rapidjson_helper.cpp
  rapidjson_helper.h
  core_code_compile.sh
  env.sh
/usr/local/include/core-code-env/
  c/*.h
  cpp/*.h
  rapidjson_helper.h
/usr/local/lib/
  libc_parse_tools.so
  libcpp_parse_tools.so
```

### Nix 环境

可以构建 core-code-env runtime 产物：

```bash
nix-build nix/core-code-env-runtime.nix
```

`nix/core-code-env-runtime.nix` 只负责 core-code-env 自己的 runtime 输出，不负责完整 HydroOJ rootfs。

完整沙箱 rootfs 需要在外层组合这些内容：

- `coreCodeEnvRuntime`
- 编译器和解释器：`gcc`、`nodejs`、`typescript`、`go`、`gotools`、`openjdk` 等
- C 语言额外依赖：`pkg-config`、`glib`、`glib.dev`、`uthash`
- 必要的 include/lib 暴露路径和 wrapper

当前部署中的外层 `rebuild_hydro_rootfs.sh` 已经在做这件事。`core-code-env-runtime.nix` 中的 `passthru.sandboxRuntimeInputs` 只是元数据，不会改变 runtime 输出，也不会自动修改现有沙箱。

## 各语言注意点

- C：`c_header` 默认包含 `glib.h` 和 `uthash.h`，编译时需要 `pkg-config --cflags --libs glib-2.0`。
- C++：依赖 `libcpp_parse_tools.so`、RapidJSON helper 和 runtime 头文件。
- Java：依赖 JDK 和 JNI，本地 runtime 会构建 `libjava_parse_module.so`。
- Python：依赖 `python3-dev`，本地 runtime 会构建 `py_parse_module*.so`。
- TypeScript：依赖 `tsc` 和 Node.js，生成器会提供最小 Node 类型 shim 以便临时 workspace 编译。
- JavaScript：依赖 Node.js。
- Go：依赖 Go 和 `goimports`。

## 开发指南

新增或修改语言时，通常改这些文件：

```text
code_gen/languages/<lang>/common.py    # 类型映射、workspace 准备、编译运行
code_gen/languages/<lang>/solution.py  # 普通函数题
code_gen/languages/<lang>/system.py    # 系统设计题
code_gen/languages/<lang>/main.py      # 语言级入口
runtimes/<lang>/                       # 语言 runtime
```

并在 [code_gen/core/language_registry.py](code_gen/core/language_registry.py) 注册语言入口和命名风格。

## 质量检查

建议提交前运行：

```bash
python3 -m py_compile code_gen/*.py code_gen/core/*.py code_gen/cli/*.py code_gen/languages/*/*.py
python3 code_gen/generate_fast.py
python3 code_gen/test_and_save.py
python3 -m code_gen.cli.test_and_save
bash -n scripts/*.sh
```

如果机器上缺少某个语言环境，对应语言会失败；先运行 `scripts/setup_dev_env.sh` 或单独安装对应依赖。

## 常见问题

### `glib.h: No such file or directory`

安装 GLib 开发包和 `pkg-config`：

```bash
sudo apt install -y pkg-config libglib2.0-dev
```

### `uthash.h: No such file or directory`

```bash
sudo apt install -y uthash-dev
```

### `Python.h: No such file or directory`

```bash
sudo apt install -y python3-dev
```

### Java JNI 构建失败 / `JAVA_HOME` 未设置

```bash
bash scripts/setup_java.sh
```

或手动设置：

```bash
export JAVA_HOME=/path/to/jdk
```

### `goimports is not found in PATH`

```bash
bash scripts/setup_goimports.sh
```

### `tsc is not found in PATH`

```bash
bash scripts/setup_node_ts.sh
```

## 备注

- `result/` 是生成产物，可以删除后重新生成。
- `.tmp/` 是临时工作目录，可以删除。
- `runtimes/` 是生成器运行依赖，不要在未更新路径解析和安装脚本的情况下删除。
