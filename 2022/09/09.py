from math import copysign
from collections import deque

dir_map = {'R': 1+0j, 'L': -1+0j, 'U': 0+1j, 'D': 0-1j}

instructions = [(dir_map[dir], int(dist)) for dir, dist in (line.split() for line in open("2022/09/input.txt").read().splitlines())]

def one_step(rope, dir):
    new_rope = deque([rope.popleft() + dir])
    # now the pieces follow the one in front
    while rope:
        head = new_rope[-1]
        tail = rope.popleft()
        delta = head - tail
        if abs(delta.real) > 1 or abs(delta.imag) > 1:
            tail += complex(
                max(-1, min(1, delta.real)),  # Move real part one step closer
                max(-1, min(1, delta.imag)))  # Move imaginary part one step closer
        new_rope.append(tail)
    return new_rope

def simulate(instructions, rope_len):
    rope = deque([0+0j] * rope_len)
    tail_set = {0+0j}
    for i, (dir, dist) in enumerate(instructions):
        for _ in range(dist):
            rope = one_step(rope, dir)
            tail_set.add(rope[-1])
        # print(f'rope after instruction {i+1}:')
        # print_rope(rope)
    return tail_set

def print_tail_set(tail_set):
    min_x = min(t.real for t in tail_set)
    max_x = max(t.real for t in tail_set)
    min_y = min(t.imag for t in tail_set)
    max_y = max(t.imag for t in tail_set)
    for y in range(int(max_y), int(min_y) - 1, -1):
        for x in range(int(min_x), int(max_x) + 1):
            print('X' if x + y * 1j in tail_set else '.', end='')
        print()

def print_rope(rope):
    min_x = min(t.real for t in rope)
    max_x = max(t.real for t in rope)
    min_y = min(t.imag for t in rope)
    max_y = max(t.imag for t in rope)
    for y in range(int(max_y), int(min_y) - 1, -1):
        for x in range(int(min_x), int(max_x) + 1):
            if x + y * 1j in rope:
                print(rope.index(x + y * 1j), end='')
            else:
                print('.', end='')
        print()
    print()

print('part 1:', len(simulate(instructions, 2)))
print('part 2:', len(simulate(instructions, 10)))