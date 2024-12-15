grid_str, instructions = open('2024/15/input.txt').read().split('\n\n')
instructions = instructions.replace('\n', '')

grid = {(x, y): c for y, line in enumerate(grid_str.splitlines()) for x, c in enumerate(line)}

grid2_map = {'#': '##', 'O': '[]', '.': '..', '@': '@.'}
grid2 = {(x*2 + i, y): grid2_map[c][i] for (x, y), c in grid.items() for i in range(2)}

dir_map = {'<': (-1, 0), '>': (1, 0), '^': (0, -1), 'v': (0, 1)}

def print_grid(grid):
    height, width = max(y for x, y in grid) + 1, max(x for x, y in grid) + 1
    for y in range(height):
        for x in range(width):
            print(grid[(x, y)], end='')
        print()

def take_step(grid, coord_list, dir):
    stuck = False
    orig_gird = grid.copy()
    while coord_list and not stuck:
        source = coord_list[-1]
        x, y = source
        sym_to_move = grid[source]
        dx, dy = dir_map[dir]
        dest = (x + dx, y + dy)
        sym_at_dest = grid[dest]
        if sym_at_dest == '#':
            stuck = True
        elif sym_at_dest == '.':
            grid[dest] = sym_to_move
            grid[source] = '.'
            coord_list.pop()
        elif sym_at_dest == 'O':
            coord_list.append(dest)
        elif sym_at_dest == '[':
            coord_list.append(dest)
            coord_list.append((dest[0]+1, dest[1]))
        elif sym_at_dest == ']':
            coord_list.append(dest)
            coord_list.append((dest[0]-1, dest[1]))
        else:
            raise Exception("Invalid move")
    return grid if not stuck else orig_gird

def walk(grid, instructions, debug=False):
    if debug: 
        print(f'Initial grid:')
        print_grid(grid)
    for i, instr in enumerate(instructions):
        if debug: print(f'Instruction {i}: {instr}')
        robot = next(k for k, v in grid.items() if v == '@')
        grid = take_step(grid, [robot], instr)
        if debug: 
            print_grid(grid)
            print()
    if debug: 
        print(f'Final grid:')
        print_grid(grid)
    return grid

def score(grid):
    return sum(k[0] + 100*k[1] for k, v in grid.items() if v in 'O[')

print('part 1:', score(walk(grid, instructions, debug=False)))
print('part 2:', score(walk(grid2, instructions, debug=False)))

