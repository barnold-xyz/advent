import math, re

dirs, _, *graph = open("08/input.txt").read().split('\n')
graph = {n: d for n, *d in [re.findall(r'\w+', s) for s in graph]}
start = [n for n in graph if n.endswith('A')]

def solve(pos, i=0):
    while not pos.endswith('Z'):
        dir = dirs[i % len(dirs)]
        pos = graph[pos][dir=='R']
        i += 1
    return i

print(math.lcm(*map(solve, start)))