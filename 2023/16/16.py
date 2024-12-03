data = open("2023/16/input.txt").read()

mirror_grid = [list(row) for row in data.split('\n')]

def grid_to_str(grid):
    return '\n'.join([''.join(str(cell) for cell in row) for row in grid])

def beam_grid_to_str(beam_grid):
    return '\n'.join([''.join([str(sum(cell)) for cell in row]) for row in beam_grid])

# beam_grid[y][x] = list of beams and their directions passing through (x, y)
beam_grid = [[[0,0,0,0] for _ in row] for row in mirror_grid]
dir_map = dict(zip('UDLR', range(4)))

def propogate_beam(x, y, dir):
    stack = [(x, y, dir, 0)]
    while stack:
        x, y, dir, counter = stack.pop()
        if counter > 1000000:
            print("hit max counter")
            return

        if y < 0 or y >= len(mirror_grid) or x < 0 or x >= len(mirror_grid[0]):
            continue

        if beam_grid[y][x][dir_map[dir]]:
            print(f"found dupe at ({x}, {y}) in direction {dir}")
            continue

        beam_grid[y][x][dir_map[dir]] = 1
        #print(f"propogating beam at ({x}, {y}) in direction {dir}")

        if mirror_grid[y][x] == '.':
            if dir == 'U': stack.append((x, y - 1, 'U', counter + 1))
            elif dir == 'D': stack.append((x, y + 1, 'D', counter + 1))
            elif dir == 'L': stack.append((x - 1, y, 'L', counter + 1))
            elif dir == 'R': stack.append((x + 1, y, 'R', counter + 1))
        elif mirror_grid[y][x] == '/':
            if dir == 'U': stack.append((x + 1, y, 'R', counter + 1))
            elif dir == 'D': stack.append((x - 1, y, 'L', counter + 1))
            elif dir == 'L': stack.append((x, y + 1, 'D', counter + 1))
            elif dir == 'R': stack.append((x, y - 1, 'U', counter + 1))
        elif mirror_grid[y][x] == '\\':
            if dir == 'U': stack.append((x - 1, y, 'L', counter + 1))
            elif dir == 'D': stack.append((x + 1, y, 'R', counter + 1))
            elif dir == 'L': stack.append((x, y - 1, 'U', counter + 1))
            elif dir == 'R': stack.append((x, y + 1, 'D', counter + 1))
        elif mirror_grid[y][x] == '|':
            if dir == 'U': stack.append((x, y - 1, 'U', counter + 1))
            elif dir == 'D': stack.append((x, y + 1, 'D', counter + 1))
            elif dir == 'L' or dir == 'R':
                stack.append((x, y - 1, 'U', counter + 1))
                stack.append((x, y + 1, 'D', counter + 1))
        elif mirror_grid[y][x] == '-':
            if dir == 'U' or dir == 'D':
                stack.append((x - 1, y, 'L', counter + 1))
                stack.append((x + 1, y, 'R', counter + 1))
            elif dir == 'L': stack.append((x - 1, y, 'L', counter + 1))
            elif dir == 'R': stack.append((x + 1, y, 'R', counter + 1))

def count_energized(beam_grid):
    return sum([sum(cell) > 0 for row in beam_grid for cell in row])

print(grid_to_str(mirror_grid))

propogate_beam(0, 0, 'R')
print('\n')
print(beam_grid_to_str(beam_grid))
print(count_energized(beam_grid))