#!/usr/bin/env python3
"""forth_interp - Stack-based Forth interpreter with definitions and control flow."""
import sys

class Forth:
    def __init__(self):
        self.stack = []
        self.words = {}
        self.builtins = {
            "+": lambda s: s.append(s.pop() + s.pop()),
            "-": lambda s: (b := s.pop(), a := s.pop(), s.append(a - b)),
            "*": lambda s: s.append(s.pop() * s.pop()),
            "/": lambda s: (b := s.pop(), a := s.pop(), s.append(a // b)),
            "mod": lambda s: (b := s.pop(), a := s.pop(), s.append(a % b)),
            "dup": lambda s: s.append(s[-1]),
            "drop": lambda s: s.pop(),
            "swap": lambda s: (s.append(s.pop(-2))),
            "over": lambda s: s.append(s[-2]),
            "rot": lambda s: s.append(s.pop(-3)),
            "=": lambda s: s.append(-1 if s.pop() == s.pop() else 0),
            "<": lambda s: (b := s.pop(), a := s.pop(), s.append(-1 if a < b else 0)),
            ">": lambda s: (b := s.pop(), a := s.pop(), s.append(-1 if a > b else 0)),
            ".": lambda s: None,  # print top
            "cr": lambda s: None,
        }
    def run(self, code):
        tokens = code.lower().split()
        i = 0
        while i < len(tokens):
            t = tokens[i]
            if t == ":":
                name = tokens[i+1]
                body = []
                i += 2
                while tokens[i] != ";":
                    body.append(tokens[i])
                    i += 1
                self.words[name] = body
            elif t == "if":
                then_b, else_b = [], []
                i += 1
                current = then_b
                depth = 1
                while depth > 0:
                    if tokens[i] == "if": depth += 1
                    elif tokens[i] == "then": depth -= 1; i += 1; continue
                    elif tokens[i] == "else" and depth == 1:
                        current = else_b; i += 1; continue
                    current.append(tokens[i])
                    i += 1
                cond = self.stack.pop()
                self._exec(then_b if cond != 0 else else_b)
                continue
            else:
                self._exec_one(t)
            i += 1
    def _exec(self, tokens):
        i = 0
        while i < len(tokens):
            t = tokens[i]
            if t == "if":
                then_b, else_b = [], []
                i += 1
                current = then_b
                depth = 1
                while depth > 0:
                    if tokens[i] == "if": depth += 1
                    elif tokens[i] == "then": depth -= 1; i += 1; continue
                    elif tokens[i] == "else" and depth == 1:
                        current = else_b; i += 1; continue
                    current.append(tokens[i])
                    i += 1
                cond = self.stack.pop()
                self._exec(then_b if cond != 0 else else_b)
                continue
            self._exec_one(t)
            i += 1
    def _exec_one(self, t):
        if t in self.words:
            self._exec(self.words[t])
        elif t in self.builtins:
            self.builtins[t](self.stack)
        else:
            try: self.stack.append(int(t))
            except: raise ValueError(f"unknown: {t}")

def test():
    f = Forth()
    f.run("3 4 +")
    assert f.stack == [7]
    f.stack.clear()
    f.run("10 3 - 2 *")
    assert f.stack == [14]
    f.stack.clear()
    f.run(": square dup * ;")
    f.run("5 square")
    assert f.stack == [25]
    f.stack.clear()
    f.run("1 if 42 else 99 then")
    assert f.stack == [42]
    f.stack.clear()
    f.run("0 if 42 else 99 then")
    assert f.stack == [99]
    print("forth_interp: all tests passed")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("Usage: forth_interp.py --test")
