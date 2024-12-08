from math import prod
import itertools

data = open("2024/07/input.txt").read().split('\n')

def add(x,y): return x+y
def mult(x,y): return x*y
def concat(x,y): return int(str(x) + str(y))
fn_list_part1 = [add, mult]
fn_list_part2 = [add, mult, concat]

def parse_line(line):
    target, args = line.split(':')
    target = int(target)
    args = list(map(int, args.strip().split(' ')))
    return target, args

def test_line(line, fn_list):
    target, args = parse_line(line)
    stack = [args]
    while stack:
        current = stack.pop()
        if len(current) == 1:
            if current[0] == target:
                return target
        else:
            if current[0] <= target: 
                [stack.append([fn(current[0], current[1])] + current[2:]) for fn in fn_list]
    return 0
    
print(sum(test_line(line, fn_list_part1) for line in data))
print(sum(test_line(line, fn_list_part2) for line in data))
