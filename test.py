from forth_interp import Forth
f = Forth()
f.execute("3 4 + .")
assert f.output == ["7"]
f2 = Forth()
f2.execute("10 3 - .")
assert f2.output == ["7"]
f3 = Forth()
f3.execute(": SQUARE DUP * ; 5 SQUARE .")
assert f3.output == ["25"]
f4 = Forth()
f4.execute("1 2 SWAP . .")
assert f4.output == ["1", "2"]
f5 = Forth()
f5.execute("3 4 OVER . . .")
assert f5.output == ["3", "4", "3"]
print("forth_interp tests passed")
