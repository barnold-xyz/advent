from collections import defaultdict
from heapq import heappop, heappush

grid = {i+j*1j: c for i,r in enumerate(open('2024/16/input.txt'))
                  for j,c in enumerate(r) if c != '#'}

start, = (p for p in grid if grid[p] in 'S')

seen = []
best = 1e9
dist = defaultdict(lambda: 1e9)
todo = [(0, t:=0, start, 1j, [start])]

while todo:
    score, _, pos, dir, path = heappop(todo)

    if score > dist[pos, dir]: continue
    else: dist[pos, dir] = score

    if grid[pos] == 'E' and score <= best:
        seen += path
        best = score

    for rot, pts in (1, 1), (1j, 1001), (-1j, 1001):
        new = pos + dir*rot
        if new in grid:
            heappush(todo, (score + pts, t := t+1,
                new, dir*rot, path + [new]))

print(best, len(set(seen)))