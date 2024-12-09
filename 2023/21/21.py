from collections import defaultdict

data = open("2023/21/test.txt").read()

graph = {}
# each entry in positions is a dict of (row, col) tuples that the elf could be at after each step and how many times
positions = []

for row, line in enumerate(data.split('\n')):
    for col, cell in enumerate(line):
        graph[(row, col)] = cell
        if cell == 'S':
            positions.append({(row, col): 1})
            graph[(row, col)] = '.'

width = len(data.split('\n')[0])
height = len(data.split('\n'))

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def print_map(grid, positions):
    for row in range(height):
        for col in range(width):
            if (row, col) in positions:
                print('O', end='')
            else:
                print(grid[(row, col)], end='')
        print()

def take_step_old(graph, positions):
    return list(set((row + d[0], col + d[1]) for row, col in positions for d in directions 
                    if graph.get((row + d[0], col + d[1]), '') == '.'))

def take_step(graph, positions):
    new_positions = defaultdict(int)
    for (row, col) in positions:
        for d in directions:
            new_row, new_col = row + d[0], col + d[1]
            if graph.get((new_row % height, new_col % width), '') == '.':
                new_positions[(new_row, new_col)] += 1
    return new_positions

def walk(graph, positions, steps):
    for i in range(steps):
        positions.append(take_step(graph, positions[-1]))
        if i>0 and i % 10000 == 0:
            print(i)
    return positions

def test(graph, positions):
    print(positions[0])
    print_map(graph, positions[0])
    positions = take_step(graph, positions[0])
    print()
    print_map(graph, positions)

def test2(graph, positions):
    for steps in [6, 10, 50, 100, 500, 1000, 5000]:
        pos = walk(graph, positions, steps)
        print(f'steps: {steps}, len: {len(pos[-1])}')

def pt1(graph, positions):
    positions = walk(graph, positions, 64)
    #print(positions[-1])
    print(len(positions[-1]))

def pt2(graph, positions):
    positions = walk(graph, positions, 26501365)
    print(len(positions[-1]))

#test(graph, positions)
print(len(walk(graph, positions, 500)[-1])); quit()
test2(graph, positions); quit()
pt1(graph, positions)
pt2(graph, positions)
#positions = walk(graph, positions, 64)
#print_map(graph, positions[-1])
#print(len(positions[-1]))