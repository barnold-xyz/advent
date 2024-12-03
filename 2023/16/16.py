data = open("2023/16/test.txt").read()

mirror_grid = [list(row) for row in data.split('\n')]

def grid_to_str(grid):
    return '\n'.join([''.join(str(cell) for cell in row) for row in grid])
    #return '\n'.join([row for row in grid])

# beam_grid[y][x] = list of beams and their directions passing through (x, y)
beam_grid = [[' ' for _ in row] for row in mirror_grid]
#beam_grid = [[[0,0,0,0] for _ in row] for row in mirror_grid]
#dir_map= dict(zip('UDLR', range(4)))

def propogate_beam(x, y, dir):
    if y < 0 or y >= len(mirror_grid) or x < 0 or x >= len(mirror_grid[0]): return

    if dir in beam_grid[y][x]: return
    
    beam_grid[y][x] += (dir)

    if mirror_grid[y][x] == '.':
        if dir == 'U': propogate_beam(x, y - 1, 'U')
        elif dir == 'D': propogate_beam(x, y + 1, 'D')
        elif dir == 'L': propogate_beam(x - 1, y, 'L')
        elif dir == 'R': propogate_beam(x + 1, y, 'R')
    if mirror_grid[y][x] == '/':
        if dir == 'U': propogate_beam(x + 1, y, 'R')
        elif dir == 'D': propogate_beam(x - 1, y, 'L')
        elif dir == 'L': propogate_beam(x, y + 1, 'D')
        elif dir == 'R': propogate_beam(x, y - 1, 'U')
    elif mirror_grid[y][x] == '\\':
        if dir == 'U': propogate_beam(x - 1, y, 'L')
        elif dir == 'D': propogate_beam(x + 1, y, 'R')
        elif dir == 'L': propogate_beam(x, y - 1, 'U')
        elif dir == 'R': propogate_beam(x, y + 1, 'D')
    elif mirror_grid[y][x] == '|':
        if dir == 'U': propogate_beam(x, y - 1, 'U')
        elif dir == 'D': propogate_beam(x, y + 1, 'D')
        elif dir == 'L' or dir == 'R': 
            propogate_beam(x, y - 1, 'U')
            propogate_beam(x, y + 1, 'D')
    elif mirror_grid[y][x] == '-':
        if dir == 'U' or dir == 'D':
            propogate_beam(x - 1, y, 'L')
            propogate_beam(x + 1, y, 'R')
        elif dir == 'L': propogate_beam(x - 1, y, 'L')
        elif dir == 'R': propogate_beam(x + 1, y, 'R')

def count_energized(beam_grid):
    return sum([len(cell)>1 for row in beam_grid for cell in row])

print(grid_to_str(mirror_grid))

propogate_beam(0, 0, 'R')
print('\n')
#print(grid_to_str(beam_grid))
print(beam_grid)
print(count_energized(beam_grid))