from math import prod
import itertools

data = open("2024/07/input.txt").read().split('\n')

def add(x,y): return x+y
def mult(x,y): return x*y
fn_list = [add, mult]

def parse_line(line):
    target, args = line.split(':')
    target = int(target)
    args = list(map(int, args.strip().split(' ')))
    return target, args

def test_line(line):
    target, args = parse_line(line)
    stack = [args]
    while stack:
        current = stack.pop()
        if len(current) == 1:
            if current[0] == target:
                return target
        else: 
            [stack.append([fn(current[0], current[1])] + current[2:]) for fn in fn_list]
    return 0
    
print(sum(test_line(line) for line in data))

