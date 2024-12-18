# https://gitlab.com/RedPixel/aoc2022/-/blob/main/day15/day15b.py
from parse import parse
from z3 import *

with open("2022/15/input.txt") as f:
    ls = f.read().splitlines()
sensors = [parse("Sensor at x={:d}, y={:d}: closest beacon is at x={:d}, y={:d}", l) for l in ls]

s = z3.Solver()
x = Int('x')
y = Int('y')
s.add(x >= 0, x <= 4000000)
s.add(y >= 0, y <= 4000000) 
for sx, sy, bx, by in sensors:
    d = abs(sx-bx) + abs(sy-by)
    s.add(Abs(sx-x) + Abs(sy-y) > d)
s.check()
m = s.model()
print(m[x].as_long()*4000000 + m[y].as_long())
print(s.check)
print(s.model())