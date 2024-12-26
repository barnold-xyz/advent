from functools import lru_cache
from frozendict import frozendict

codes = open('2024/21/test.txt').read().splitlines()

keypad = frozendict({
    (0, 0): '7',
    (1, 0): '8',
    (2, 0): '9',
    (0, 1): '4',
    (1, 1): '5',
    (2, 1): '6',
    (0, 2): '1',
    (1, 2): '2',
    (2, 2): '3',
    (1, 3): '0',
    (2, 3): 'A'
})

arrows = frozendict({
    (1, 1): '^',
    (2, 1): 'A',
    (0, 2): '<',
    (1, 2): 'v',
    (2, 2): '>'
})

dir_map = frozendict({ 'v': (0, 1), '^': (0, -1), '>': (1, 0), '<': (-1, 0) })


def find_paths(grid, start, end):
    def dfs(current, path, directions):
        if current == end:
            paths.append(directions)
            return
        x, y = current
        for direction, (dx, dy) in dir_map.items():
            nx, ny = x + dx, y + dy
            if (nx, ny) in grid and (nx, ny) not in path:
                dfs((nx, ny), path + [(nx, ny)], directions + direction)

    paths = []
    dfs(start, [start], '')
    return [p for p in paths if len(p) == min(map(len, paths))]

@lru_cache(maxsize=None)
def find_all_paths(grid):
    all_paths = {}
    points = list(grid.keys())
    for i in range(len(points)):
        for j in range(len(points)):
            start, end = points[i], points[j]
            paths = find_paths(grid, start, end)
            all_paths[(start, end)] = paths
    return all_paths

def get_inst_to_keypad(code):
    pos = keypad_map['A']
    inst = []
    for char in code:
        paths = keypad_paths[(pos, keypad_map[char])]
        paths = [p + 'A' for p in paths if len(p) == min(map(len, paths))]
        inst.append(paths)
        pos = keypad_map[char]
    return inst

# check each path and take the one with the shortest length
def get_inst_to_arrows(path):
    pos = arrow_map['A']
    for p1 in path:
        for char in p1:
            paths = arrow_paths[(pos, arrow_map[char])]
            paths = [p + 'A' for p in paths if len(p) == min(map(len, paths))]
            pos = arrow_map[char]


keypad_paths = find_all_paths(keypad)
arrow_paths = find_all_paths(arrows)

keypad_map = frozendict({v: k for k, v in keypad.items()})
arrow_map = frozendict({v: k for k, v in arrows.items()})

breakpoint()

def part1(codes):
    scores = []
    for code in codes:
        print(code)
        print(get_inst_to_keypad(code))
        print([get_inst_to_arrows(p) for p in get_inst_to_keypad(code)])
        insts = next(i for i in insts if len(i) == min(map(len, insts)))
        scores.append(len(insts) * int(code[:-1]))
    print(scores)
    return sum(scores)

print(part1(codes))


