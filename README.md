# 计算器后端（Flask + SQLite）

前后端分离计算器作业的后端部分。提供表达式计算接口和历史记录持久化（SQLite）。

## 技术栈

- Python + Flask：REST API
- Flask-CORS：允许前端跨域访问
- SQLite：历史记录持久化（无需额外安装数据库）

## 快速启动

```bash
pip install -r requirements.txt
python app.py
```

启动成功后在控制台看到 `Running on http://0.0.0.0:5000`，
前端配置的 `API_BASE_URL` 为 `http://localhost:5000/api`。

## API 一览

| 方法   | 路径                  | 说明                             |
| ------ | --------------------- | -------------------------------- |
| POST   | `/api/calculate`      | 计算表达式，写入历史记录         |
| GET    | `/api/history`        | 获取全部历史记录                 |
| DELETE | `/api/history/<id>`   | 删除单条历史记录                 |
| DELETE | `/api/history`        | 清空全部历史记录                 |

错误时返回 400，`error` 字段为中文提示（如 “除数不能为零”）。