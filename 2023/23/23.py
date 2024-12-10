from collections import defaultdict
from colorama import init, Fore, Back, Style
init()

data = open("2023/23/input.txt").read()

grid = {(row, col): cell for row, line in enumerate(data.split('\n')) for col, cell in enumerate(line)}
height = max(row for row, col in grid) + 1
width = max(col for row, col in grid) + 1

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
dir_map = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1)}
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
            debug = row == 3 and col == 3
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
                if start != end:
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


def find_all_paths(graph, start, end, path=[], path_length=0):
    path = path + [start]
    if start == end:
        return [(path, path_length)]
    if start not in graph:
        return []
    paths = []
    for node, length in graph[start]:
        if node not in path:
            new_paths = find_all_paths(graph, node, end, path, path_length + length)
            for p in new_paths:
                paths.append(p)
    return paths



def test():
    print_map(grid)
    print()
    print(f'(1,1): {graph[(1,1)]}')
    print(f'(3,3): {graph[(3,3)]}')
    print(f'(4,3): {graph[(4,3)]}')
    print(f'(5,3): {graph[(5,3)]}')

graph = build_graph(grid, prune=True)
#test()

start = (0, 1)
#end = (3,3)
end = (height-1, width - 2)

all_paths = find_all_paths(graph, start, end)
print(sorted(l for _, l in all_paths))

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
    breakpoint() 
    #print_map(grid, all_paths[0][0])

