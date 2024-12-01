import networkx as nx

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

def find_cycle_with_start(graph, start_pos):
    cycles = nx.cycle_basis(graph)
    for cycle in cycles:
        if start_pos in cycle:
            return cycle
    return None

def calculate_area(cycle):
    n = len(cycle)
    area = 0
    for i in range(n):
        x1, y1 = cycle[i]
        x2, y2 = cycle[(i + 1) % n]
        area += x1 * y2 - y1 * x2
    return abs(area) / 2

graph, start_pos = parse_graph(data)
cycle = find_cycle_with_start(graph, start_pos)

if cycle:
    area = calculate_area(cycle)
    print("Area enclosed by the cycle:", area - len(cycle) / 2 + 1)
else:
    print("No cycle found containing the start position.")