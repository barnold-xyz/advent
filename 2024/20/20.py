from collections import deque, Counter

grid = {(x, y): c for y, line in enumerate(open('2024/20/input.txt')) for x, c in enumerate(line.strip())}

def bfs_path(grid, start, end):
    queue = deque([(start, [])])
    visited = set()
    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == end:
            return path + [(x, y)]
        if (x, y) in visited:
            continue
        visited.add((x, y))
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if grid.get((new_x, new_y)) != '#':
                queue.append(((new_x, new_y), path + [(x, y)]))
    return []

def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def find_cheats(path, cheat_len=2):
    cheats = {}
    for i in range(0, len(path)-1):
        x, y = path[i]
        for j in range(i+1, len(path)):
            xc, yc = path[j]
            d = dist((x, y), (xc, yc))
            if d > cheat_len or d == j - i:
                continue
            savings = j - i - d
            if savings > 0:
                cheats[((x, y), (xc, yc))] = savings
    return cheats

start = next(k for k, v in grid.items() if v == 'S')
end = next(k for k, v in grid.items() if v == 'E')
base_path = bfs_path(grid, start, end)
print(f'start: {start}, end: {end}, base path length: {len(base_path)}')

cheats = find_cheats(base_path)
print('part 1:', sum(1 for c in cheats.values() if c >= 100))
cheats2 = find_cheats(base_path, cheat_len=20)
print('part 2:', sum(1 for c in cheats2.values() if c >= 100))


