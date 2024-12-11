import numpy as np
from z3 import *

data = [[int(n.strip()) for n in line.split(',')] for line in open("2023/24/input.txt").read().replace('@', ',').split('\n')]

data = [[(a, b, c), (x, y, z)] for a, b, c, x, y, z in data]

def intersects_xy(a, b):
    (ax, ay, az), (avx, avy, avz) = a
    (bx, by, bz), (bvx, bvy, bvz) = b
    
    #https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
    # y = ax + c
    # y = bx + d
    # x = (d - c) / (a - b)
    # y = a * x + c
    a = avy / avx
    c = ay - a * ax
    b = bvy / bvx
    d = by - b * bx
    
    if a == b:
        return False
    
    x = (d - c) / (a - b)
    y = a * x + c

    return (x, y, 0)

def test_intersection(a, b, lbound, ubound, check_z=False):
    (ax, ay, az), (avx, avy, avz) = a
    (bx, by, bz), (bvx, bvy, bvz) = b
    
    intersection = intersects_xy(a, b)
    if not intersection:
        return False
    
    # check that it's inside the bounds
    if not lbound <= intersection[0] <= ubound:
        return False
    if not lbound <= intersection[1] <= ubound:
        return False
    
    time_a = (intersection[0] - ax) / avx
    time_b = (intersection[0] - bx) / bvx

    if not(time_a > 0 and time_b > 0):
        return False
    
    if check_z:
        if not az + time_a * avz == bz + time_b * bvz:
            return False
        
    return True

def test(data):
    lbound = 7
    ubound = 27
    for i in range(len(data)):
        for j in range(i):
            inter_loc = intersects_xy(data[i], data[j])
            inter_test = test_intersection(data[i], data[j], lbound, ubound)
            print(f'A: {data[i]}\tB: {data[j]}\tIntersection: {inter_loc}\tTest: {inter_test}')
        
def part1(data):
    lbound = 200000000000000
    ubound = 400000000000000
    results = []
    for i in range(len(data)):
        for j in range(i):
            results.append(test_intersection(data[i], data[j], lbound, ubound, check_z=False))
    print(sum(results))

# thanks claude
def part2(data):
    # Create symbolic variables for rock's initial position and velocity
    rx, ry, rz = Ints('rx ry rz')
    rvx, rvy, rvz = Ints('rvx rvy rvz')
    
    # Create solver
    s = Solver()
    
    # For each hailstone, create time variable and add constraints
    for i, ((hx, hy, hz), (hvx, hvy, hvz)) in enumerate(data):
        t = Int(f't{i}')
        
        # Collision equations for x, y, z dimensions
        s.add(t >= 0)
        s.add(rx + rvx * t == hx + hvx * t)
        s.add(ry + rvy * t == hy + hvy * t)
        s.add(rz + rvz * t == hz + hvz * t)
    
    # Check if solution exists
    if s.check() == sat:
        m = s.model()
        return sum([m.evaluate(rx).as_long(), 
                    m.evaluate(ry).as_long(), 
                    m.evaluate(rz).as_long()])
    
    return None

#test(data)
part1(data)
print(part2(data))