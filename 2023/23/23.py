from collections import defaultdict
from colorama import init, Fore, Back, Style
init()

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
dir_map = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1)}

data = open("2023/23/test.txt").read()

grid = {(row, col): cell for row, line in enumerate(data.split('\n')) for col, cell in enumerate(line)}
grid_pt2 = {k: '.' if v in dir_map else v for k, v in grid.items()}

height = max(row for row, col in grid) + 1
width = max(col for row, col in grid) + 1

#rev_dir_map = {'^': (1, 0), 'v': (-1, 0), '<': (0, 1), '>': (0, -1)}

def print_map(grid, positions=[], highlight=[]):
    for row in range(height):
        for col in range(width):
            if (row, col) in highlight:
                print(Fore.RED + grid[(row, col)] + Style.RESET_ALL, end='')
            elif (row, col) in positions:
                print('O', end='')
            else:
                print(grid[(row, col)], end='')
        print()


# graph is a dict of (row, col) tuples to the connected cells
def build_graph(grid, prune=True):
    debug = False
    graph = defaultdict(list)
    for row in range(height):
        for col in range(width):
            #debug = row == 3 and col == 3
            cell = grid[(row, col)]
            if cell == '#':
                continue
            elif cell in dir_map:
                graph[(row, col)].append(((row + dir_map[cell][0], col + dir_map[cell][1]), 1))
            elif cell == '.':  # If the cell is empty, attempt to add all 4 directions
                for d in directions:
                    new_row, new_col = row + d[0], col + d[1]
                    new_cell = grid.get((new_row, new_col), '')
                    if debug: print(f"Checking direction {d}")
                    if debug: print(f"new_cell: {new_cell}")

                    if new_cell == '.' or dir_map.get(new_cell, '') == d:
                        if debug: print(f"Adding edge from {(row, col)} to {(new_row, new_col)}")
                        graph[(row, col)].append(((new_row, new_col), 1))
                    elif debug: print(f"Skipping direction {d}")

    # prune the graph: if a cell has only 2 neighbors and both are '.', remove it and connect its neighbors
    def prune_graph(graph):
        def is_chain_node(node):
            result = len(graph[node]) == 2 and all(grid[neighbor[0]] == '.' for neighbor in graph[node])
            return result

        def find_chain(node):
            chain = [node]
            while is_chain_node(chain[-1]):
                next_node = next(n for n, _ in graph[chain[-1]] if n not in chain)
                chain.append(next_node)
            return chain

        for node in list(graph):
            if node not in graph: continue
            if is_chain_node(node):
                chain = find_chain(node)
                start, end = chain[0], chain[-1]
                if start != end and len(chain) > 3:
                    total_length = len(chain) - 1
                    graph[start] = [(n, l) for n, l in graph[start] if n != chain[1]]
                    graph[end] = [(n, l) for n, l in graph[end] if n != chain[-2]]
                    graph[start].append((end, total_length))
                    graph[end].append((start, total_length))
                    for chain_node in chain[1:-1]:
                        if chain_node in graph:
                            del graph[chain_node]
        return graph

    if prune:
        graph = prune_graph(graph)
    return graph


def find_all_paths(graph, start, end):
    stack = [(start, [start], 0)]
    paths = []
    while stack:
        (vertex, path, path_length) = stack.pop()
        for next_vertex, length in graph[vertex]:
            if next_vertex not in path:
                if next_vertex == end:
                    paths.append((path + [next_vertex], path_length + length))
                else:
                    stack.append((next_vertex, path + [next_vertex], path_length + length))
    return paths

def compress_graph(grid):
    # Create a compressed graph by finding intersection points
    graph = defaultdict(list)
    intersections = set()
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

    # Find intersection points (nodes with more than 2 neighbors)
    for (row, col), cell in grid.items():
        if cell == '#':
            continue
        
        neighbors = 0
        for dr, dc in directions:
            new_pos = (row + dr, col + dc)
            if grid.get(new_pos, '#') != '#':
                neighbors += 1
        
        if neighbors > 2:
            intersections.add((row, col))
    
    print(f"Intersections found: {intersections}")

    # Connect intersections
    for (row, col) in intersections:
        for dr, dc in directions:
            path_length = 0
            cur_pos = (row + dr, col + dc)
            while grid.get(cur_pos, '#') != '#':
                path_length += 1
                cur_pos = (cur_pos[0] + dr, cur_pos[1] + dc)
                if cur_pos in intersections:
                    graph[(row, col)].append((cur_pos, path_length))
                    graph[cur_pos].append(((row, col), path_length))
                    break
                if grid.get(cur_pos, '#') == '#':
                    break
    
    print(f"Compressed graph: {dict(graph)}")
    return graph

def find_longest_path(graph, start, end):
    # Initialize memoization dictionary
    memo = {}

    # Stack to simulate recursion
    stack = [(start, {start}, 0)]  # (current node, visited nodes, current path length)
    max_length = float('-inf')
    total_nodes = len(graph)

    while stack:
        node, visited, path_length = stack.pop()
        visited_key = frozenset(visited)

        # If we've reached the end, update max_length
        if node == end:
            max_length = max(max_length, path_length)
            print(f"Found path from {start} to {end} with length {path_length}, max_length: {max_length}")
            continue

        # If the result is already memoized, use it
        if (node, visited_key) in memo:
            max_length = max(max_length, path_length + memo[(node, visited_key)])
            continue

        # Calculate the number of nodes left to visit
        nodes_left = total_nodes - len(visited)

        # If the potential maximum path length is less than the current max_length, skip this path
        if path_length + nodes_left <= max_length:
            print(f"Skipping path from {node} with length {path_length} and {nodes_left} nodes left")
            continue

        # Explore all possible next nodes
        for next_node, length in graph[node]:
            if next_node not in visited:
                # Create a new visited set
                new_visited = visited | {next_node}
                
                # Push the next state onto the stack
                stack.append((next_node, new_visited, path_length + length))

        # Memoize the result
        memo[(node, visited_key)] = max_length - path_length

    return max_length

# Prepare the grid (removing slope restrictions)
grid_pt2 = {k: '.' if v in dir_map else v for k, v in grid.items()}

# Find start and end
start = (0, 1)
end = (height-1, width - 2)

# Compress the graph
print('Compressing graph...')
#compressed_graph = compress_graph(grid_pt2)
compressed_graph = build_graph(grid_pt2, prune=False)
# Find the longest path
print('Finding longest path...')
longest_path = find_longest_path(compressed_graph, start, end)
print(f"Longest path in Part 2: {longest_path}")

quit()

graph = build_graph(grid, prune=True)
#graph = build_graph(grid, prune=False)
all_paths = find_all_paths(graph, start, end)
print(sorted(l for _, l in all_paths))

#graph_pt2 = build_graph(grid_pt2, prune=True)
graph_pt2 = build_graph(grid_pt2, prune=False)
#all_paths_pt2 = find_all_paths(graph_pt2, start, end)
#print(f'number of paths: {len(all_paths_pt2)}')
#print(f' max path length: {max(l for _, l in all_paths_pt2)}')
#longest_path = find_longest_path_iterative(graph_pt2, start, end)
print(f'longest path: {longest_path}')

def debug_pt_1():
    all_paths = find_all_paths(graph, start, end)
    for path, path_len in all_paths:
        print(f'showing path for length {path_len}')
        print_map(grid, path)
        print()

    # compare the first path to the one with length 81
    print(sorted(l for _, l in all_paths))
    path0 = next(path for path, length in all_paths if length == 94)
    path1 = next(path for path, length in all_paths if length == 73)
    path2 = next(path for path, length in all_paths if length == 81)
    print(f'in path1 but not path2: {set(path1) - set(path2)}')
    print(f'in path2 but not path1: {set(path2) - set(path1)}')
    print(f'in both paths: {set(path1) & set(path2)}')
    print(f'in path1 and path2 but not path0: {set(path1) & set(path2) - set(path0)}')

    investigate = set(path1) & set(path2) - set(path0)
    print_map(grid, highlight=list(investigate))
    print()
    print_map(grid, highlight=[start, end])
    breakpoint() 
    #print_map(grid, all_paths[0][0])
