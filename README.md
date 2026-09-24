# 计算器后端（Flask + SQLite）

前后端分离计算器作业的后端部分。提供表达式计算接口和历史记录持久化（SQLite）。
所有核心计算（表达式解析、优先级、括号、一元负号、除零/非法表达式处理）都在本后端完成。

## 技术栈

- Python + Flask：REST API
- Flask-CORS：允许前端跨域访问
- SQLite：历史记录持久化（无需额外安装数据库服务）

## 运行时环境

- Python 3.10+（本项目在 Python 3.14 上开发测试）
- 依赖见 `requirements.txt`：`flask`、`flask-cors`

## 安装方法

```bash
pip install -r requirements.txt
```

## 启动方法

```bash
python app.py
```

启动成功后控制台显示 `Running on http://0.0.0.0:5000`。

## 配置说明

- 服务端口：`app.py` 末尾 `app.run(host='0.0.0.0', port=5000)`，可修改。
- 数据库文件路径：`app.py` 中 `DB_PATH`，默认与 `app.py` 同目录下的 `calculator.db`。
- 跨域：`CORS(app)` 允许所有来源访问（部署时前端与后端域名不同，必须开启）。

## 数据库初始化

无需手动建库。首次启动时 `init_db()` 会自动创建数据库文件与 `history` 表：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | INTEGER PRIMARY KEY AUTOINCREMENT | 主键 |
| expression | TEXT | 计算表达式 |
| result | TEXT | 计算结果 |
| created_at | TEXT | 记录时间 `YYYY-MM-DD HH:MM:SS` |

如需清空数据，删除 `calculator.db` 文件后重启即可，或调用 `DELETE /api/history`。

## 前后端连接方法

前端通过 `https://localhost:5000/api`（或部署后的公开地址）访问以下接口：

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/api/calculate` | 计算表达式，写入历史 |
| GET | `/api/history` | 获取历史记录 |
| DELETE | `/api/history/<id>` | 删除单条历史 |
| DELETE | `/api/history` | 清空全部历史 |

错误时返回 HTTP 400，`error` 字段为中文提示（如“除数不能为零”）。

## 部署（PythonAnywhere / gunicorn）

仓库内置 `wsgi.py`（`from app import app as application`），可直接用于
gunicorn 或 PythonAnywhere 手动配置的 WSGI 入口。