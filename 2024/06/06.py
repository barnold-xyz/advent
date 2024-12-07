# load the data into a grid
grid = {(x, y): char for y, line in enumerate(open("2024/06/input.txt").read().split('\n')) for x, char in enumerate(line)}

dirs = '^>v<'
moves = [(0, -1), (1, 0), (0, 1), (-1, 0)]
guard_pos = next((pos for pos, char in grid.items() if char in dirs))
dir = grid[guard_pos]
grid[guard_pos] = '.'
visted = set()

def print_grid():
    print()
    for y in range(10):
        for x in range(10):
            if (x, y) == guard_pos:
                print(dir, end='')
            else:
                print(grid.get((x, y), '.'), end='')
        print()
    print()

steps = 0
while True: # and steps < 15:
    visted.add(guard_pos)

    # attempt to move forward
    dr, dc = moves[dirs.index(dir)]
    new_pos = (guard_pos[0] + dr, guard_pos[1] + dc)
    if grid.get(new_pos) is None:  break

    if grid[new_pos] == '#':  # turn
        dir = dirs[(dirs.index(dir) + 1) % len(dirs)]
    else:
        guard_pos = new_pos
    steps += 1
    print_grid()
    
print(len(visted))  