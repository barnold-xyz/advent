codes = open('2024/21/test.txt').read().splitlines()

keypad = {
    '7': (0, 0),
    '8': (1, 0),
    '9': (2, 0),
    '4': (0, 1),
    '5': (1, 1),
    '6': (2, 1),
    '1': (0, 2),
    '2': (1, 2),
    '3': (2, 2),
    '0': (1, 3),
    'A': (2, 3)
}

arrows = {
    '^': (1, 1),
    'A': (2, 1),
    '<': (0, 2),
    'v': (1, 2),
    '>': (2, 2),
}

# get the best path between each pair of keys on the keypad
def get_path(start, end):
    (sx, sy), (ex, ey) = start, end
    path = '>' * max(ex - sx, 0)
    path += abs(ey - sy) * ('v' if ey > sy else '^')
    path += '<' * max(sx - ex, 0)
    return path

# first move left, then vertical (unless it will pass through (0,2), in which case move vertical first)
def get_path(start, end):
    (sx, sy), (ex, ey) = start, end
    path = '<' * max(sx - ex, 0)
    path += abs(ey - sy) * ('v' if ey > sy else '^')
    path += '>' * max(ex - sx, 0)

    ## check if path will pass through (0,2)
    if sy == 2 and ex == 0:
        path = abs(ey - sy) * ('v' if ey > sy else '^')
        path += '<' * max(sx - ex, 0)

    return path
    

def get_inst(code, target_map):
    inst = ''
    pos = target_map['A']
    for char in code:
        inst += get_path(pos, target_map[char]) + 'A'
        pos = target_map[char]
    return inst

def part1(codes):
    scores = []
    for code in codes:
        print(code)
        print(get_inst(code, keypad))
        print(get_inst(get_inst(code, keypad), arrows))
        print(get_inst(get_inst(get_inst(code, keypad), arrows), arrows))
        print()
        scores.append(len(get_inst(get_inst(get_inst(code, keypad), arrows), arrows)) * int(code[:-1]))
    print(scores)
    print(sum(scores))

part1(codes)