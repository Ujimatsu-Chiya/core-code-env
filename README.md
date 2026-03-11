# core-code-env

多语言代码模板生成与本地验证框架，面向 LeetCode 风格题目，支持两类模板：

- `solution`：普通函数题（单函数入口）
- `system`：系统设计题（类/对象调用序列）

当前已对齐并支持的语言：

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
├── code_gen/                  # 代码生成主逻辑（Python）
│   ├── core/                  # 跨语言共享逻辑（注册表、编排、测试工具）
│   ├── languages/<lang>/      # 各语言生成器（common/solution/system/main）
│   ├── cli/                   # CLI 入口
│   ├── runtime_layout.py      # 运行时模板路径解析
│   └── test_and_save.py       # 主入口（调用 orchestrator）
├── runtimes/<lang>/           # 各语言运行时模板/桥接代码
├── result/
│   ├── solution/              # 普通函数题生成结果
│   └── system/                # 系统设计题生成结果
├── script/                    # 环境安装脚本（Python/Java/Go/Node）
├── rapidjson_helper.cpp       # C/C++/Java 解析桥通用依赖
└── gen.sh                     # 一键生成脚本
```

## 快速开始

### 1) 基础依赖

至少需要：

- Python 3.10+（推荐 3.12）
- `gcc` / `g++`
- Node.js（含 `npm`）
- Java JDK（建议 21）
- Go（建议 1.21+）

Ubuntu 参考安装：

```bash
sudo apt update
sudo apt install -y python3 python3-dev build-essential openjdk-21-jdk golang-go nodejs npm
npm i -g typescript
go install golang.org/x/tools/cmd/goimports@latest
```

可选脚本（会修改 `~/.bashrc`）：

```bash
bash script/setup_python.sh
bash script/setup_java.sh
bash script/setup_go.sh
bash script/setup_goimports.sh
bash script/setup_node_ts.sh

# 一键安装（会依次调用上述脚本）
bash script/setup_dev_env.sh
```

### 2) 运行生成

项目根目录执行：

```bash
python3 -m code_gen.cli.test_and_save
```

或：

```bash
python3 code_gen/test_and_save.py
```

或：

```bash
./gen.sh
```

生成结果输出到：

- `result/solution/main_body.<lang>`
- `result/solution/main_trailer.<lang>`
- `result/system/main_body.<lang>`
- `result/system/main_trailer.<lang>`

## 入口说明

统一入口：

- `python3 -m code_gen.cli.test_and_save`
- `python3 code_gen/test_and_save.py`

语言级调试入口：

- `python3 -m code_gen.languages.c.main`
- `python3 -m code_gen.languages.cpp.main`
- `python3 -m code_gen.languages.java.main`
- `python3 -m code_gen.languages.py.main`
- `python3 -m code_gen.languages.ts.main`
- `python3 -m code_gen.languages.js.main`
- `python3 -m code_gen.languages.go.main`

## 运行时模板路径解析

运行时目录通过 `code_gen/runtime_layout.py` 解析，优先级如下：

1. `CODE_GEN_RUNTIME_<LANG>_PATH`
2. `CODE_GEN_RUNTIME_ROOT` + `<lang>`
3. `runtimes/<lang>`
4. 旧路径兼容目录名（仅路径解析保留，不再依赖旧源码结构）

示例：

```bash
export CODE_GEN_RUNTIME_ROOT=/abs/path/to/runtimes
export CODE_GEN_RUNTIME_CPP_PATH=/abs/path/to/custom/cpp_runtime
```

## 临时目录与输出清理

框架执行时会在 `.tmp/` 下创建隔离工作目录，避免并发冲突。

可覆盖临时根目录：

```bash
export CODE_GEN_TMP_ROOT=/abs/path/to/tmp_root
```

每次生成前会清理目标目录中旧的 `main_body.*` / `main_trailer.*` 文件。

## 各语言编译/运行要点

- C / C++：依赖 `gcc` / `g++` 和 `runtimes/c`、`runtimes/cpp` 中的桥接文件。
- Java：若 `runtimes/java/libjava_parse_module.so` 不存在，会尝试构建本地库，需要 `JAVA_HOME` 与 JNI 头文件。
- Python：若 `runtimes/py/py_parse_module*.so` 不存在，会通过 `setup.py build` 构建，需要 `python3-dev`（`Python.h`）。
- TypeScript：需要 `tsc`（`npm i -g typescript`）。
- JavaScript：需要 `node`。
- Go：需要 `go` 与 `goimports`。

## 开发指南

### 新增/修改某语言生成器

建议遵循该语言目录结构：

- `common.py`：类型映射、运行时准备、编译运行函数
- `solution.py`：函数题模板生成与测试
- `system.py`：系统题模板生成与测试
- `main.py`：语言级导出与本地示例入口

并在以下位置接入：

- `code_gen/core/language_registry.py`：注册 `solution/system` 测试函数与命名风格

### 编排层

`code_gen/core/orchestrator.py` 提供：

- `test_solution(...)`
- `test_system(...)`
- `main()`

## 质量检查

建议在提交前执行：

```bash
python3 -m py_compile code_gen/*.py code_gen/core/*.py code_gen/cli/*.py code_gen/languages/*/*.py
python3 code_gen/test_and_save.py
python3 -m code_gen.cli.test_and_save
```

## 常见问题

### `Python.h: No such file or directory`

安装 Python 开发头文件：

```bash
sudo apt install -y python3-dev
```

### Java JNI 构建失败 / `JAVA_HOME` 未设置

```bash
export JAVA_HOME=/path/to/jdk
```

或运行：

```bash
bash script/setup_java.sh
```

### `goimports is not found in PATH`

```bash
go install golang.org/x/tools/cmd/goimports@latest
export PATH="$PATH:$(go env GOPATH)/bin"
```

### `tsc is not found in PATH`

```bash
npm i -g typescript
```

## 备注

- `runtimes/` 下的模板/桥接代码是生成器运行依赖，不建议随意删除。
- `result/` 与 `.tmp/` 属于产物目录，可按需清理。
