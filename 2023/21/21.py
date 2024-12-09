data = open("2023/21/input.txt").read()

graph = {}
# each entry in positions is a list of (row, col) tuples that the elf could be at after each step
positions = []

for row, line in enumerate(data.split('\n')):
    for col, cell in enumerate(line):
        graph[(row, col)] = cell
        if cell == 'S':
            positions.append([(row, col)])
            graph[(row, col)] = '.'

width = len(data.split('\n')[0])
height = len(data.split('\n'))

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def print_map(grid, pos_list):
    for row in range(height):
        for col in range(width):
            if (row, col) in pos_list:
                print('O', end='')
            else:
                print(grid[(row, col)], end='')
        print()

def take_step(graph, positions):
    return list(set((row + d[0], col + d[1]) for row, col in positions for d in directions 
                    if graph.get((row + d[0], col + d[1]), '') == '.'))

def walk(graph, positions, steps):
    for _ in range(steps):
        positions.append(take_step(graph, positions[-1]))
    return positions

#print_map(graph, positions[0])

positions = walk(graph, positions, 64)
#print_map(graph, positions[-1])
print(len(positions[-1]))