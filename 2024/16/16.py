from math import inf
from collections import deque
import heapq
import networkx as nx

grid = {(x,y): c for y, row in enumerate(open('2024/16/test3.txt')) for x, c in enumerate(row.strip())}
height = max(y for x, y in grid.keys()) + 1
width = max(x for x, y in grid.keys()) + 1
start = next(k for k, v in grid.items() if v == 'S')
end = next(k for k, v in grid.items() if v == 'E')
grid[start] = '.'
grid[end] = '.'

def print_grid(path=[]):
    for y in range(height):
        for x in range(width):
            if (x, y) in path:
                print('\033[91mo\033[0m', end='')
            else:
                print(grid.get((x, y), ' '), end='')
        print()

def dfs(start, end, start_dir=(0, 1)):
    # Priority queue: (priority, steps, current_position, direction, path)
    heap = []
    heapq.heappush(heap, (0, 0, start, start_dir, [start]))  # (direction_changes, steps, position, direction, path)
    
    all_paths = []
    best_steps = inf

    while heap:
        direction_changes, steps, pos, direction, path = heapq.heappop(heap)

        if pos == end:
            cost = steps + 1000*direction_changes
            all_paths.append((cost, steps, direction_changes, path))
            best_steps = min(best_steps, cost)
            print(f'Found path with {steps} steps and {direction_changes} direction changes, best is {best_steps}')
            continue

        x, y = pos
        for new_dir in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_pos = (x + new_dir[0], y + new_dir[1])
            if grid.get(new_pos) == '.' and new_pos not in path:
                new_direction_changes = direction_changes + (new_dir != direction)
                new_steps = steps + 1 
                if new_steps < best_steps:
                    heapq.heappush(heap, (new_direction_changes, new_steps, new_pos, new_dir, path + [new_pos]))
                    # print(f"Heap size: {len(heap)}, Direction changes: {new_direction_changes}, Steps: {new_steps}, Best: {best_steps}")

    return all_paths

# build a directed graph from the grid. 1 node for each (x,y) position x incoming direction
def graph_from_grid(grid):
    G = nx.DiGraph()
    for y in range(height):
        for x in range(width):
            if grid.get((x, y)) == '.':
                for dir in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    G.add_node((x, y, dir))
                    for new_dir in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        new_pos = (x + new_dir[0], y + new_dir[1])
                        if grid.get(new_pos) == '.':
                            G.add_edge((x, y, dir), (x + new_dir[0], y + new_dir[1], new_dir), weight=1+1000*(dir != new_dir))
                
    return G

def prune_graph(G, start, ends):
    # remove all nodes that are not reachable from start
    reachable = nx.descendants(G, start)
    for node in list(G.nodes):
        if node not in reachable:
            G.remove_node(node)
            if node in ends:
                ends.remove(node)
                print(f"Removed end node {node}")
    # if an node can reach any of the ends it can stay
    reachable = set()
    for end in ends:
        reachable |= nx.descendants(G, end)
    for node in list(G.nodes):
        if node not in reachable:
            G.remove_node(node)

    return G

def dijkstra(start, end, start_dir=(0, 1)):
    # Priority queue: (total_cost, steps, current_position, direction, path)
    heap = []
    heapq.heappush(heap, (0, 0, start, start_dir, [start]))  # (total_cost, steps, position, direction, path)

    visited = {}  # Tracks the minimum cost to reach each (pos, direction)
    all_paths = []

    while heap:
        total_cost, steps, pos, direction, path = heapq.heappop(heap)

        # Check if we've already visited this (pos, direction) with a cheaper cost
        if (pos, direction) in visited and visited[(pos, direction)] <= total_cost:
            continue

        # Mark this state as visited
        visited[(pos, direction)] = total_cost

        # If we've reached the end, record the path
        if pos == end:
            all_paths.append((total_cost, steps, path))
            print(f"Found path with cost {total_cost}, steps {steps}, path: {path}")
            continue  # Do not break; other paths may have the same cost

        # Explore neighbors
        x, y = pos
        for new_dir in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_pos = (x + new_dir[0], y + new_dir[1])
            if grid.get(new_pos) == '.':  # Valid neighbor
                # Calculate costs
                new_direction_changes = (new_dir != direction)
                new_steps = steps + 1
                new_cost = total_cost + 1 + 1000 * new_direction_changes

                # Push the new state to the heap
                heapq.heappush(heap, (new_cost, new_steps, new_pos, new_dir, path + [new_pos]))
    
    return all_paths

def too_slow():
    paths = dfs(start, end)
    best_path = min(paths, key=lambda x: x[0])
    print_grid(best_path[-1])
    print(best_path[0])

paths = dijkstra(start, end)
print_grid(paths[0][-1])
print(paths[0][0])
quit()


graph = graph_from_grid(grid)
print(graph)

start_node = (start[0], start[1], (0, 1))
end_node = ((end[0], end[1], (1, 0)))
# end_node = ((end[0], end[1], (0, -1)))

path = nx.shortest_path(graph, source=start_node, target=end_node, weight='weight')
distance = nx.shortest_path_length(graph, source=start_node, target=end_node, weight='weight')
# print(f'Shortest path: {path}')
print(f'Shortest path distance: {distance}')
# print_grid([(x,y) for x,y,d in path])
# print(path)
# too_slow()