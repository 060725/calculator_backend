# 代码规范（后端）

本后端仓库遵循以下约定，便于助教与协作者阅读：

## Python

- 使用 Python 3.10+，统一 UTF-8 编码，文件头部标注 `# -*- coding: utf-8 -*-`。
- 缩进使用 4 个空格，不使用 Tab。
- 命名规范：
  - 函数、变量：`snake_case`（如 `get_conn`、`record_id`）
  - 类：`PascalCase`（如 `Parser`）
  - 常量：`UPPER_SNAKE_CASE`（如 `DB_PATH`）
- 每个函数必须有 docstring，说明功能、参数与返回值。
- 异常处理：业务错误抛出 `ValueError` 并在 API 层转为 400 响应中文提示。

## 数据库

- 表名、字段名使用小写加下划线。
- 时间统一使用 `YYYY-MM-DD HH:MM:SS` 字符串格式。
- 所有数据库操作使用参数化 SQL，禁止字符串拼接。

## Git 提交

- 提交信息用英文，简明描述改动（如 `Initial commit: calculator backend with Flask + SQLite`）。
- 不提交 `calculator.db`、`__pycache__` 等运行产物（见 `.gitignore`）。