from itertools import zip_longest
from functools import cmp_to_key

def read_input(file):
    return [[eval(element) for element in line.split('\n')] for line in open(file).read().split('\n\n')]

def comp(left, right): 
    # print(f'comparing {left} and {right}')
    if left is None: return -1
    if right is None: return 1
    if isinstance(left, int) and isinstance(right, list): return comp([left], right)
    if isinstance(left, list) and isinstance(right, int): return comp(left, [right])
    if isinstance(left, int) and isinstance(right, int): 
        if left == right: return 0
        else: return 1 if left > right else -1

    if isinstance(left, list) and isinstance(right, list):
        for l, r in zip_longest(left, right):
            if comp(l, r) == 1: return 1
            if comp(l, r) == -1: return -1
        return 0
    return 0

def part1():
    data = read_input('2022/13/input.txt')
    print('part 1:', sum(i+1 for i in range(len(data)) if comp(data[i][0], data[i][1]) == -1))

def part2():
    data = [item for sublist in read_input('2022/13/input.txt') for item in sublist]
    data += [[[2]],[[6]]]

    result = sorted(data, key=cmp_to_key(comp))
    print('part 2:', (result.index([[2]])+1) * (result.index([[6]])+1))

part1()
part2()