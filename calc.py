# -*- coding: utf-8 -*-
"""表达式解析与求值模块。

支持：加 +、减 -、乘 ×/*、除 ÷//、括号 ()、一元负号（如 3*-2）、小数。
优先级：括号 > 一元负号 > 乘除 > 加减，符合常规数学规则。
除数为零或表达式非法时抛出 ValueError（带中文提示）。
"""
import re

_TOKEN_RE = re.compile(r'\s*(\d+(?:\.\d+)?|[+\-*/×÷()])')
_NUM_RE = re.compile(r'\d+(?:\.\d+)?')


class Parser:
    """递归下降解析器：expr -> term -> factor。"""

    def __init__(self, text):
        self.tokens = []
        pos = 0
        while pos < len(text):
            m = _TOKEN_RE.match(text, pos)
            if not m:
                raise ValueError('表达式无效')
            self.tokens.append(m.group(1))
            pos = m.end()
        if not self.tokens:
            raise ValueError('表达式无效')
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def take(self):
        tok = self.peek()
        self.pos += 1
        return tok

    def parse(self):
        value = self.parse_expr()
        if self.peek() is not None:
            raise ValueError('表达式无效')
        return value

    # expr := term (('+' | '-') term)*
    def parse_expr(self):
        value = self.parse_term()
        while self.peek() in ('+', '-'):
            op = self.take()
            rhs = self.parse_term()
            value = value + rhs if op == '+' else value - rhs
        return value

    # term := factor (('*' | '/' | '×' | '÷') factor)*
    def parse_term(self):
        value = self.parse_factor()
        while self.peek() in ('*', '/', '×', '÷'):
            op = self.take()
            rhs = self.parse_factor()
            if op in ('/', '÷'):
                if rhs == 0:
                    raise ValueError('除数不能为零')
                value /= rhs
            else:
                value *= rhs
        return value

    # factor := ('+'|'-') factor | '(' expr ')' | number
    def parse_factor(self):
        tok = self.peek()
        if tok is None:
            raise ValueError('表达式无效')
        if tok in ('+', '-'):
            self.take()
            val = self.parse_factor()
            return val if tok == '+' else -val
        if tok == '(':
            self.take()
            val = self.parse_expr()
            if self.take() != ')':
                raise ValueError('表达式无效')
            return val
        if _NUM_RE.fullmatch(tok):
            self.take()
            return float(tok)
        raise ValueError('表达式无效')


def fmt(value):
    """把浮点结果格式化为友好字符串：6.0 -> '6'，0.30000000000000004 -> '0.3'。"""
    if abs(value - round(value)) < 1e-12:
        return str(int(round(value)))
    return f'{value:.10f}'.rstrip('0').rstrip('.')


def evaluate(expression):
    """求值入口。失败抛 ValueError。"""
    return fmt(Parser(expression).parse())