import networkx as nx
import numpy as np

data = open("2023/10/input.txt").read().strip().split('\n')

def parse_graph(data):
    graph = nx.Graph()
    start_pos = None

    # Initialize nodes
    for r, line in enumerate(data):
        for c, char in enumerate(line):
            graph.add_node((r, c))
            if char == 'S': start_pos = (r, c)

    # Add edges
    for r, line in enumerate(data):
        for c, char in enumerate(line):
            if char == '|':
                if (r+1, c) in graph and data[r+1][c] in 'S|JL':
                    graph.add_edge((r, c), (r+1, c))
                if (r-1, c) in graph and data[r-1][c] in 'S|F7':
                    graph.add_edge((r, c), (r-1, c))
            elif char == '-':
                if (r, c+1) in graph and data[r][c+1] in 'S-7J':
                    graph.add_edge((r, c), (r, c+1))
                if (r, c-1) in graph and data[r][c-1] in 'S-LF':
                    graph.add_edge((r, c), (r, c-1))
            elif char == 'L':
                if (r, c+1) in graph and data[r][c+1] in 'S-7J':
                    graph.add_edge((r, c), (r, c+1))
                if (r-1, c) in graph and data[r-1][c] in 'S|F7':
                    graph.add_edge((r, c), (r-1, c))
            elif char == 'J':
                if (r-1, c) in graph and data[r-1][c] in 'S|F7':
                    graph.add_edge((r, c), (r-1, c))
                if (r, c-1) in graph and data[r][c-1] in 'S-LF':
                    graph.add_edge((r, c), (r, c-1))
            elif char == '7':
                if (r, c-1) in graph and data[r][c-1] in 'S-LF':
                    graph.add_edge((r, c), (r, c-1))
                if (r+1, c) in graph and data[r+1][c] in 'S|JL':
                    graph.add_edge((r, c), (r+1, c))
            elif char == 'F':
                if (r+1, c) in graph and data[r+1][c] in 'S|JL':
                    graph.add_edge((r, c), (r+1, c))
                if (r, c+1) in graph and data[r][c+1] in 'S-7J':
                    graph.add_edge((r, c), (r, c+1))

    return graph, start_pos

graph, start_pos = parse_graph(data)
distances = nx.single_source_shortest_path_length(graph, start_pos)

print(max(distances.values()))

'''
rows, cols = len(data), len(data[0])
grid = np.full((len(data), len(data[0])), -1)  # Initialize with -1 to indicate unreachable nodes


for (r, c), distance in distances.items():
    grid[r, c] = distance

# Print the grid
for row in grid:
    print(' '.join(f'{val:2}' for val in row))

'''