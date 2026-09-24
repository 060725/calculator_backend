# -*- coding: utf-8 -*-
"""WSGI 入口，用于 PythonAnywhere / gunicorn 等生产部署。

用法（本地 gunicorn 测试）：
    gunicorn wsgi:application

在 PythonAnywhere 的 WSGI 配置文件中：
    1. 将项目目录加入 sys.path
    2. 写入：from wsgi import application
"""
from app import app as application

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000)