grid_str, instructions = open('2024/15/input.txt').read().split('\n\n')
grid = {(x, y): c for y, line in enumerate(grid_str.splitlines()) for x, c in enumerate(line)}
instructions = instructions.replace('\n', '')

height, width = max(y for x, y in grid) + 1, max(x for x, y in grid) + 1
dir_map = {'<': (-1, 0), '>': (1, 0), '^': (0, -1), 'v': (0, 1)}

def print_grid(grid):
    for y in range(height):
        for x in range(width):
            print(grid[(x, y)], end='')
        print()

def take_step(grid, coord_to_move, dir, stuck=False):
    if stuck:
        return grid, stuck
    x, y = coord_to_move
    sym_to_move = grid[coord_to_move]
    dx, dy = dir_map[dir]
    new_pos = (x + dx, y + dy)
    if grid[new_pos] == '#': # can't move
        return grid, True
    elif grid[new_pos] == '.': # open space
        grid[new_pos] = sym_to_move
        grid[coord_to_move] = '.'
        return grid, False
    elif grid[new_pos] == 'O': # moving a box
        grid, stuck = take_step(grid, new_pos, dir)
        if stuck:
            return grid, stuck
        else:
            return take_step(grid, coord_to_move, dir)
    else:
        raise Exception("Invalid move")

def walk(grid, instructions, debug=False):
    print(f'Initial grid:')
    print_grid(grid)
    for i, instr in enumerate(instructions):
        if debug: print(f'Instruction {i}: {instr}')
        robot = next(k for k, v in grid.items() if v == '@')
        grid, _ = take_step(grid, robot, instr)
        if debug: 
            print_grid(grid)
            print()
    print(f'Final grid:')
    print_grid(grid)
    return grid

def score(grid):
    return sum(k[0] + 100*k[1] for k, v in grid.items() if v == 'O')

# print_grid(grid)
# print(instructions)

print('part 1:', score(walk(grid, instructions)))

