# 代码规范（后端）

## 规范来源（Source of This Standard）

本仓库代码规范参照 Python 社区官方标准 **PEP 8 — Style Guide for Python Code**
（https://peps.python.org/pep-0008/）与 **PEP 257 — Docstring Conventions**
（https://peps.python.org/pep-0257/）制定，并针对本项目（Flask + SQLite 后端）做了少量裁剪。

## 基础约定

- 使用 Python 3.10+，统一 UTF-8 编码。
- 缩进使用 4 个空格，不使用 Tab；行宽不超过 79~99 字符（PEP 8 建议 79，本代码采用 99）。
- 命名规范（PEP 8）：
  - 函数、变量：`snake_case`（如 `get_conn`、`record_id`）
  - 类：`PascalCase`（如 `Parser`）
  - 常量：`UPPER_SNAKE_CASE`（如 `DB_PATH`）
  - 私有成员：下划线前缀（如 `_TOKEN_RE`、`self._pos`）
- 每个公开函数必须有 docstring（PEP 257），说明功能、参数与返回值。

## 业务与异常

- 业务错误抛出 `ValueError`，API 层统一转为 HTTP 400 + 中文提示 `error` 字段。
- 参数化 SQL 查询，禁止字符串拼接，防止 SQL 注入。
- 数据库连接必须在 `finally` 中关闭。

## 数据库

- 表名、字段名使用小写下划线（如 `history`、`created_at`）。
- 时间统一 `YYYY-MM-DD HH:MM:SS` 字符串格式。

## Git 提交

- 提交信息用英文，简明描述改动（示例：`Initial commit: calculator backend with Flask + SQLite`）。
- 不提交运行产物（`calculator.db`、`__pycache__/` 等），见 `.gitignore`。