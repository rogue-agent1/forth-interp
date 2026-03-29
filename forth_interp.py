#!/usr/bin/env python3
"""Forth-like stack language interpreter."""
import sys

class Forth:
    def __init__(self):
        self.stack = []
        self.words = {}
        self.output = []
        self._builtins = {
            "+": lambda: self._binop(lambda a,b: a+b),
            "-": lambda: self._binop(lambda a,b: a-b),
            "*": lambda: self._binop(lambda a,b: a*b),
            "/": lambda: self._binop(lambda a,b: a//b),
            "mod": lambda: self._binop(lambda a,b: a%b),
            "dup": lambda: self.stack.append(self.stack[-1]),
            "drop": lambda: self.stack.pop(),
            "swap": lambda: self._swap(),
            "over": lambda: self.stack.append(self.stack[-2]),
            "rot": lambda: self._rot(),
            ".": lambda: self.output.append(str(self.stack.pop())),
            "=": lambda: self._binop(lambda a,b: -1 if a==b else 0),
            "<": lambda: self._binop(lambda a,b: -1 if a<b else 0),
            ">": lambda: self._binop(lambda a,b: -1 if a>b else 0),
            "cr": lambda: self.output.append("\n"),
            "emit": lambda: self.output.append(chr(self.stack.pop())),
        }
    def _binop(self, fn):
        b, a = self.stack.pop(), self.stack.pop()
        self.stack.append(fn(a, b))
    def _swap(self):
        self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]
    def _rot(self):
        a = self.stack.pop(-3)
        self.stack.append(a)
    def eval(self, text):
        tokens = text.split()
        i = 0
        while i < len(tokens):
            t = tokens[i].lower()
            if t == ":":
                name = tokens[i+1].lower()
                body = []
                i += 2
                while tokens[i] != ";":
                    body.append(tokens[i]); i += 1
                self.words[name] = body
            elif t in self._builtins:
                self._builtins[t]()
            elif t in self.words:
                self.eval(" ".join(self.words[t]))
            else:
                try: self.stack.append(int(t))
                except ValueError:
                    try: self.stack.append(float(t))
                    except ValueError: raise ValueError(f"Unknown: {t}")
            i += 1
        return self.output

def test():
    f = Forth()
    f.eval("3 4 + .")
    assert f.output == ["7"]
    f2 = Forth()
    f2.eval(": square dup * ;")
    f2.eval("5 square .")
    assert f2.output == ["25"]
    f3 = Forth()
    f3.eval("10 20 swap . .")
    assert f3.output == ["10", "20"]
    f4 = Forth()
    f4.eval("1 2 3 rot . . .")
    assert f4.output == ["1", "3", "2"]
    print("  forth_interp: ALL TESTS PASSED")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else:
        f = Forth()
        f.eval(": fact dup 1 > if dup 1 - fact * then ;")
        print("Forth interpreter — interactive mode not implemented")
