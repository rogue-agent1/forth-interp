#!/usr/bin/env python3
"""Minimal Forth interpreter. Zero dependencies."""

class Forth:
    def __init__(self):
        self.stack = []; self.words = {}; self.output = []

    def execute(self, text):
        tokens = text.split(); i = 0
        while i < len(tokens):
            t = tokens[i].upper()
            if t == ":":
                name = tokens[i+1].upper(); body = []
                i += 2
                while tokens[i].upper() != ";": body.append(tokens[i]); i += 1
                self.words[name] = body
            elif t in self.words:
                self.execute(" ".join(self.words[t]))
            elif t == ".": self.output.append(str(self.stack.pop()))
            elif t == ".S": self.output.append(f"<{len(self.stack)}> " + " ".join(str(x) for x in self.stack))
            elif t == "DUP": self.stack.append(self.stack[-1])
            elif t == "DROP": self.stack.pop()
            elif t == "SWAP": self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]
            elif t == "OVER": self.stack.append(self.stack[-2])
            elif t == "ROT": a = self.stack.pop(-3); self.stack.append(a)
            elif t == "+": b, a = self.stack.pop(), self.stack.pop(); self.stack.append(a + b)
            elif t == "-": b, a = self.stack.pop(), self.stack.pop(); self.stack.append(a - b)
            elif t == "*": b, a = self.stack.pop(), self.stack.pop(); self.stack.append(a * b)
            elif t == "/": b, a = self.stack.pop(), self.stack.pop(); self.stack.append(a // b)
            elif t == "MOD": b, a = self.stack.pop(), self.stack.pop(); self.stack.append(a % b)
            elif t == "=": b, a = self.stack.pop(), self.stack.pop(); self.stack.append(-1 if a == b else 0)
            elif t == "<": b, a = self.stack.pop(), self.stack.pop(); self.stack.append(-1 if a < b else 0)
            elif t == ">": b, a = self.stack.pop(), self.stack.pop(); self.stack.append(-1 if a > b else 0)
            elif t == "EMIT": self.output.append(chr(self.stack.pop()))
            elif t == "CR": self.output.append("\n")
            elif t == "ABS": self.stack.append(abs(self.stack.pop()))
            elif t == "NEGATE": self.stack.append(-self.stack.pop())
            elif t == "MAX": b, a = self.stack.pop(), self.stack.pop(); self.stack.append(max(a, b))
            elif t == "MIN": b, a = self.stack.pop(), self.stack.pop(); self.stack.append(min(a, b))
            else:
                try: self.stack.append(int(t))
                except ValueError:
                    try: self.stack.append(float(tokens[i]))
                    except ValueError: raise ValueError(f"Unknown word: {tokens[i]}")
            i += 1
        return self

    def get_output(self): return " ".join(self.output)

if __name__ == "__main__":
    f = Forth()
    f.execute("3 4 + .")
    print(f.get_output())
