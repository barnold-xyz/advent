from collections import deque, Counter

grid = {(x, y): c for y, line in enumerate(open('2024/20/input.txt')) for x, c in enumerate(line.strip())}

def print_grid(grid):
    height, width = max(y for x, y in grid) + 1, max(x for x, y in grid) + 1
    for y in range(height):
        for x in range(width):
            char = grid[(x, y)]
            if char == '.':
                print(f'\033[1;37m{char}\033[0m', end='')  # ANSI escape code for bold white
            elif char == '#':
                print(f'\033[94m{char}\033[0m', end='')  # ANSI escape code for blue
            else:
                print(char, end='')
        print()

# use BFS to find shortest path and optionally return the actual path
def bfs(grid, start, end, cheat=()):
    queue = deque([(start, 0)])
    visited = set()
    while queue:
        (x, y), dist = queue.popleft()
        if (x, y) == end:
            return dist
        if (x, y) in visited:
            continue
        visited.add((x, y))
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if grid.get((new_x, new_y)) != '#' or (new_x, new_y) == cheat:
                queue.append(((new_x, new_y), dist + 1))
    return -1

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

# find the # squares that connect 2 squares in the path
def find_cheats(grid, path):
    cheats = {}
    for i in range(0, len(path)-1):
        x, y = path[i]
        path_neighbors = [(x + dx, y + dy) for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]]
        for xc, yc in path_neighbors:
            if grid.get((xc, yc)) == '#':
                cheat_neighbors = [(xc + dx, yc + dy) for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]]
                for xcn, ycn in cheat_neighbors:
                    if (xcn, ycn) != (x, y) and (xcn, ycn) in path:
                        savings = path.index((xcn, ycn)) - path.index((x, y)) - 2
                        if savings > 0:
                            cheats[((xc, yc), (xcn, ycn))] = savings
    return cheats

start = next(k for k, v in grid.items() if v == 'S')
end = next(k for k, v in grid.items() if v == 'E')
base_path = bfs_path(grid, start, end)
print(f'start: {start}, end: {end}, base path length: {len(base_path)}')
cheats = find_cheats(grid, base_path)
# print(f'cheats: {cheats}')
print(dict(sorted(Counter(cheats.values()).items())))
print('part 1:', sum(1 for c in cheats.values() if c >= 100))
quit()

# make a list of possible cheats: if a # has at least 2 . neighbors, it is a possible cheat
possible_cheats = [k for k, v in grid.items() if v == '#' and sum(1 for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)] if grid.get((k[0] + dx, k[1] + dy)) == '#') <= 2]
cheats2 = {cheat: len(base_path) - bfs(grid, start, end, cheat) - 1 for cheat in possible_cheats if len(base_path) - bfs(grid, start, end, cheat) - 1 > 0}
print(f'len cheats: {len(cheats)}, len cheats2: {len(cheats2)}')

# print([cheat for cheat in cheats if cheat_path_savings[cheats.index(cheat)] == 0])
# print_grid(grid)
print(dict(sorted(Counter(cheats.values()).items())))
print(dict(sorted(Counter(cheats2.values()).items())))

breakpoint()