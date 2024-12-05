data = [line.split(' ') for line in open('2023/18/input.txt').read().split('\n')]

dir_map = dict(zip('RLUD', [(1, 0), (-1, 0), (0, -1), (0, 1)]))  # Updated to ensure x is horizontal and y is vertical
hex_to_dir = dict({'0':'R', '1':'D', '2':'L', '3':'U'})

def parse_part1(data):
    trench = {}
    x = y = 0
    for dir_code, length, color_code in data:
        dir = dir_map[dir_code]
        length = int(length)
        color = color_code.strip('()')
        for _ in range(length):
            trench[(x, y)] = color
            x += dir[0]
            y += dir[1]
    return trench

def parse_part2(data):
    trench = {}
    x = y = 0
    for _, _,  inst in data:
        inst = inst.strip('()#')
        length = int(inst[:5], 16)
        dir = dir_map[hex_to_dir[inst[5]]]
        for _ in range(length):
            trench[(x, y)] = '#999999'
            x += dir[0]
            y += dir[1]
    return trench

# flood fill the lagoon
def flood_fill(grid, trench, x, y, color='#123456'):
    lagoon = {}
    stack = [(x, y)]
    while stack:
        cx, cy = stack.pop()
        if (cx, cy) in lagoon or (cx, cy) not in grid or (cx, cy) in trench:
            continue
        lagoon[(cx, cy)] = color
        stack.append((cx - 1, cy))
        stack.append((cx + 1, cy))
        stack.append((cx, cy - 1))
        stack.append((cx, cy + 1))
    return lagoon

def print_data(data, x_values, y_values):
    for y in y_values:
        for x in x_values:
            print(1 * (data.get((x, y)) is not None), end='')
        print()

def print_crosses(crosses, x_values, y_values):
    for y in y_values:
        for x in x_values:
            print(crosses.get((x, y), 0), end='')
        print()

# count the number of times you cross the trench
# if you cross the trench an odd # of times, you're in the lagoon
def count_crosses(grid, trench, x_values):
    crosses = {}
    for (x, y) in grid:
        if (x, y) in trench:
            crosses[(x, y)] = 0
            continue
        count = 0
        for x2 in range(min(x_values), x):
            if (x2, y) in trench and (x2 - 1, y) not in trench:
                count += 1
        crosses[(x, y)] = count
    return crosses

def solve(trench):
    y_values = sorted(set(y for x, y in trench))
    x_values = sorted(set(x for x, y in trench))

    grid = {(x, y): None for y in y_values for x in x_values}  # Ensure grid is created with x as horizontal and y as vertical
    print(f'Grid size: {len(x_values)}x{len(y_values)}')

    crosses = count_crosses(grid, trench, x_values)
    #print_crosses(crosses)
    print(sum(1 for x in crosses if crosses[x] % 2 == 1))

    print(f'Number of trench squares: {len(trench)}')

    # choose a starting point that is inside the lagoon
    flood_start = next((x, y) for x, y in grid if crosses[(x, y)] % 2 == 1)
    print(f'Could try starting flood fill at {flood_start}')
    #lagoon = flood_fill(grid, trench, flood_start[0], flood_start[1])
    lagoon = flood_fill(grid, trench, 135,0)
    print(f'Number of lagoon squares: {len(lagoon)}')
    print(f'Total lava: {len(trench) + len(lagoon)}')

solve(parse_part1(data))
#solve(parse_part2(data))

# graph the grid in matplotlib
import matplotlib.pyplot as plt

def plot_grid(data):
    fig, ax = plt.subplots()
    for (x, y), color in data.items():
        ax.add_patch(plt.Rectangle((x, y), 1, 1, color=color))
    ax.autoscale_view()
    plt.show()