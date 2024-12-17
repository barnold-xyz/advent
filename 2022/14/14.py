import keyboard

data = open("2022/14/input.txt").read().splitlines()
data = [line.split(" -> ") for line in data]

def build_grid(data, sand_source=(500, 0)):
    grid = {sand_source: '+'}
    for line in data:
        for i in range(0, len(line) - 1):
            x1, y1 =  map(int, line[i].split(","))
            x2, y2 = map(int, line[i+1].split(","))
            # print(f'i: {i}, x1: {x1}, y1: {y1}, x2: {x2}, y2: {y2}')
            for x in range(min(x1, x2), max(x1, x2) + 1):
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    grid[(x, y)] = '#'

    # fill in the blanks
    min_x = min(x for x, y in grid)
    max_x = max(x for x, y in grid)
    min_y = min(y for x, y in grid)
    max_y = max(y for x, y in grid)
    for x in range(min_x-1, max_x + 1):
        for y in range(min_y-1, max_y + 1):
            if (x, y) not in grid:
                grid[(x, y)] = '.'
    return grid

def print_grid(grid, sand_source=(500, 0), part2=False):
    min_x = min(x for x, y in grid)
    max_x = max(x for x, y in grid)
    min_y = min(y for x, y in grid)
    max_y = max(y for x, y in grid)

    if part2:
        min_x, max_x = max(min_x, 400), min(max_x, 530)
        min_y, max_y = max(min_y, -1), min(max_y, 170)

    print(f'grid dimensions: {min_x}, {max_x}, {min_y}, {max_y}')
    for y in range(min_y-1, max_y + 2):
        for x in range(min_x-1, max_x + 2):
            char = grid.get((x, y), ' ')
            if char == '#':    
                print('\033[31m#\033[0m', end='')  # red
            elif char == 'O':
                print('\033[93mO\033[0m', end='')  # yellow
            else:
                print(char, end='')
        print()

def drip_sand(grid, sand_source=(500, 0)):
    x, y = sand_source
    max_y = max(y for _, y in grid)  # Determine the bottommost y value in the grid
    
    while True:
        # Fall downwards as long as the space below is empty
        if grid.get((x, y+1)) == '.':
            y += 1
            if y >= max_y:  # Reached the bottom of the grid
                return False
        # Move left and down if possible
        elif grid.get((x-1, y+1)) == '.':
            x -= 1
            y += 1
        # Move right and down if possible
        elif grid.get((x+1, y+1)) == '.':
            x += 1
            y += 1
        # Sand has stopped moving
        else:
            if y >= max_y:  # Reached the bottom of the grid
                return False
            else:
                grid[(x, y)] = 'O'
                # print(f'added O at {x}, {y} (max_y: {max_y})')
                return (x, y) != sand_source

def drip_sand_and_print(grid, sand_source=(500, 0)):
    while True:
        if keyboard.is_pressed('space'):
            success = drip_sand(grid, sand_source)
            print_grid(grid)
            if not success:
                break
            while keyboard.is_pressed('space'):
                pass  # wait for spacebar to be released

def fill(grid):
    count = 0
    success = True
    while success:
        success = drip_sand(grid)
        count += 1
        # print(f'count: {count}')
        # if count % 1 == 0:
        #     print_grid(grid)    
        # if count == 38: break

def extend_grid(grid, sand_source):
    min_x = min(x for x, y in grid)
    max_x = max(x for x, y in grid)
    min_y = min(y for x, y in grid)
    max_y = max(y for x, y in grid)

    for i in range(4*abs(sand_source[1] - max_y)):
        grid[(min_x - i, max_y + 2)] = '#'
        grid[(min_x + i, max_y + 2)] = '#'
        for j in range(min_y -1, max_y + 2):
            if not (min_x - i, j) in grid: grid[(min_x - i, j)] = '.'
            if not (min_x + i, j) in grid: grid[(min_x + i, j)] = '.'

print(data)
grid = build_grid(data)
sand_source = (500, 0)
grid[sand_source] = '+'  
print_grid(grid)

# part 1
fill(grid)
print_grid(grid)
print('part 1:', sum(1 for _, v in grid.items() if v == 'O'))

# part 2
extend_grid(grid, sand_source)
print_grid(grid, part2=True)
fill(grid)
print_grid(grid, part2=True)
print('part 2:', sum(1 for _, v in grid.items() if v == 'O'))