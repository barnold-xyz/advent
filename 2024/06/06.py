# load the data into a grid
grid = {(x, y): char for y, line in enumerate(open("2024/06/input.txt").read().split('\n')) for x, char in enumerate(line)}

dirs = '^>v<'
moves = [(0, -1), (1, 0), (0, 1), (-1, 0)]
guard_pos = next((pos for pos, char in grid.items() if char in dirs))
dir = grid[guard_pos]
grid[guard_pos] = '.'

def print_grid(grid, guard_pos, dir):
    print()
    for y in range(max(y for x, y in grid.keys()) + 1):
        for x in range(max(x for x, y in grid.keys()) + 1):
            if (x, y) == guard_pos:
                print(dir, end='')
            else:
                print(grid.get((x, y), '.'), end='')
        print()
    print()

def run_sim(grid, guard_pos, dir):
    steps = 0
    cells_visited = set()
    cells_plus_dir = set()
    while True: 
        if (guard_pos, dir) in cells_plus_dir:
            return {'outcome': 0, 'cells': cells_visited}

        cells_visited.add(guard_pos)
        cells_plus_dir.add((guard_pos, dir))

        # attempt to move forward
        dr, dc = moves[dirs.index(dir)]
        new_pos = (guard_pos[0] + dr, guard_pos[1] + dc)
        if grid.get(new_pos) is None:  
            return {'outcome': 1, 'cells': cells_visited}

        if grid[new_pos] == '#':  # turn
            dir = dirs[(dirs.index(dir) + 1) % len(dirs)]
        else:
            guard_pos = new_pos
        steps += 1
        #print_grid(grid, guard_pos, dir)
    
def part1(grid, guard_pos, dir):
    result = run_sim(grid, guard_pos, dir)
    print(len(result['cells']))

# this is slow but it works
def part2(grid, guard_pos, dir):
    loop_count = 0
    for y in range(max(y for x, y in grid.keys()) + 1):
        for x in range(max(x for x, y in grid.keys()) + 1):
            new_grid = grid.copy()
            new_grid[(x, y)] = '#'
            results = run_sim(new_grid, guard_pos, dir)
            if results['outcome'] == 0:
                loop_count += 1

    print(loop_count)

part1(grid, guard_pos, dir)
part2(grid, guard_pos, dir)