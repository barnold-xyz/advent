data = [line.split(' ') for line in open('2023/18/input.txt').read().split('\n')]

trench = {}
x = y = 0
dir_map = dict(zip('RLUD', [(1, 0), (-1, 0), (0, -1), (0, 1)]))  # Updated to ensure x is horizontal and y is vertical
for dir_code, length, color_code in data:
    dir = dir_map[dir_code]
    length = int(length)
    color = color_code.strip('()')
    for _ in range(length):
        trench[(x, y)] = color
        x += dir[0]
        y += dir[1]

y_values = sorted(set(y for x, y in trench))
x_values = sorted(set(x for x, y in trench))

#height = max(y for x, y in trench) + 1  # Ensure height is based on y
#width = max(x for x, y in trench) + 1  # Ensure width is based on x
grid = {(x, y): None for y in y_values for x in x_values}  # Ensure grid is created with x as horizontal and y as vertical
print(f'Grid size: {len(x_values)}x{len(y_values)}')

# flood fill the lagoon
def flood_fill(x, y, color='#123456'):
    global lagoon 
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

def print_data(data):
    for y in y_values:
        for x in x_values:
            print(1 * (data.get((x, y)) is not None), end='')
        print()

def print_crosses(crosses):
    for y in y_values:
        for x in x_values:
            print(crosses.get((x, y), 0), end='')
        print()

# count the number of times you cross the trench
# if you cross the trench an odd # of times, you're in the lagoon
crosses = {}
def count_crosses():
    for (x, y) in grid:
        if (x, y) in trench:
            crosses[(x, y)] = 0
            continue
        count = 0
        for x2 in range(min(x_values), x):
            if (x2, y) in trench and (x2 - 1, y) not in trench:
                count += 1
        crosses[(x, y)] = count

count_crosses()
#print_crosses(crosses)
print(sum(1 for x in crosses if crosses[x] % 2 == 1))

print(len(trench))
# choose a starting point that is inside the lagoon
flood_start = next((x, y) for x, y in grid if crosses[(x, y)] % 2 == 1)
print(f'Starting flood fill at {flood_start}')
#flood_fill(flood_start[0], flood_start[1])
flood_fill(5,5)
print(len(lagoon))
flood_fill(50,50)
flood_fill(135,0)
print(len(lagoon))
print(f'Total lava: {len(trench) + len(lagoon)}')

#print_data(trench)
#print()
#print_data(lagoon)

# graph the grid in matplotlib
import matplotlib.pyplot as plt

def plot_grid(data):
    fig, ax = plt.subplots()
    for (x, y), color in data.items():
        ax.add_patch(plt.Rectangle((x, y), 1, 1, color=color))
    ax.autoscale_view()
    plt.show()

plot_grid(trench)