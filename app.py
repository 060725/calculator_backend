# -*- coding: utf-8 -*-
"""计算器后端：Flask + SQLite。

API 一览（基础路径 /api）：
  POST   /api/calculate         传入 {"expression": "1+2×3"}，返回计算结果并写入历史
  GET    /api/history           获取历史记录（按时间倒序，最多 100 条）
  DELETE /api/history/<id>      删除单条历史记录
  DELETE /api/history           清空所有历史记录

历史记录保存在本地 SQLite 文件 calculator.db 中，服务重启、前端刷新后依然存在。
"""
import os
import sqlite3
from datetime import datetime

from flask import Flask, jsonify, request
from flask_cors import CORS

from calc import evaluate

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'calculator.db')

app = Flask(__name__)
CORS(app)


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS history (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                expression TEXT NOT NULL,
                result     TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


init_db()


@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json(silent=True) or {}
    expression = (data.get('expression') or '').strip()
    if not expression:
        return jsonify({'error': '表达式不能为空'}), 400
    try:
        result = evaluate(expression)
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400

    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = get_conn()
    try:
        cur = conn.execute(
            'INSERT INTO history (expression, result, created_at) VALUES (?, ?, ?)',
            (expression, result, created_at),
        )
        conn.commit()
        record_id = cur.lastrowid
    finally:
        conn.close()
    return jsonify({'id': record_id, 'expression': expression,
                    'result': result, 'created_at': created_at}), 201


@app.route('/api/history', methods=['GET'])
def history():
    conn = get_conn()
    try:
        rows = conn.execute(
            'SELECT * FROM history ORDER BY id DESC LIMIT 100'
        ).fetchall()
    finally:
        conn.close()
    return jsonify({'items': [dict(r) for r in rows]})


@app.route('/api/history/<int:rid>', methods=['DELETE'])
def delete_record(rid):
    conn = get_conn()
    try:
        conn.execute('DELETE FROM history WHERE id = ?', (rid,))
        conn.commit()
    finally:
        conn.close()
    return jsonify({'ok': True})


@app.route('/api/history', methods=['DELETE'])
def clear_history():
    conn = get_conn()
    try:
        cur = conn.execute('DELETE FROM history')
        conn.commit()
        deleted = cur.rowcount
    finally:
        conn.close()
    return jsonify({'ok': True, 'deleted': deleted})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)