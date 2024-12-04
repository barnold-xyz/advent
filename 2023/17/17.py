import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from math import inf

input_file = '2023/17/test_pt2.txt'
dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

'''
G = {(i, j, dir, consec_steps): int(c) for consec_steps in range(0,3) 
     for dir in dirs 
     for i, r in enumerate(open(input_file))
     for j, c in enumerate(r.strip())}
g = list(G.keys())

graph = nx.DiGraph()
graph.add_nodes_from(g)
print('graph has nodes:', len(graph.nodes()))
nodes1 = graph.nodes()
print(graph)
for (i, j, dir, consec_steps) in g:
    for di, dj in dirs:
        if (di, dj) == (-dir[0], -dir[1]): continue
        neighbor = (i + di, j + dj, (di, dj), 0 if (di, dj) != dir else consec_steps + 1)
        if neighbor in g:
            graph.add_edge((i, j, dir, consec_steps), neighbor, weight=G[neighbor])
print(graph)

start = (0, 0, dirs[0], 0)
end_nodes = [(max(i for i, j, *_ in g), max(j for i, j, *_ in g), dir, consec_steps) 
             for consec_steps in range(0,2)
             for dir in dirs]
# find the distance from start to every other node
dist = nx.single_source_dijkstra_path_length(graph, source=start, weight='weight')

# find the dist to any end node
print([dist.get(end) for end in end_nodes])
'''
# part2: need to move a min of 4 blocks and a max of 10 blocks
G = {(i, j, dir): int(c) 
     for dir in dirs 
     for i, r in enumerate(open(input_file))
     for j, c in enumerate(r.strip())}
g = list(G.keys())

graph2 = nx.DiGraph()
graph2.add_nodes_from(g)
print(graph2)
for (i, j, dir) in g:
    for di, dj in set(dirs) - {(dir[0], dir[1]),(-dir[0], -dir[1])}:
        skipped_nodes = [(i+di*dist, j+dj*dist, (di, dj)) for dist in range(1, 4)]
        skipped_wt = sum(G[n] for n in skipped_nodes if n in g)

        neighbors = [(i+di*dist, j+dj*dist, (di, dj)) for dist in range(4, 11)]
        [graph2.add_edge((i, j, dir), n, weight=G[n]+skipped_wt) for n in neighbors if n in g]

print(graph2)

start_nodes = [(0, 0, d) for d in dirs]
end_nodes = [(max(i for i, j, *_ in g), max(j for i, j, *_ in g), dir) for dir in dirs]
dist = nx.single_source_dijkstra_path_length(graph2, source=start_nodes[0], weight='weight')

# print the grid: 1 if reachable else 0   
for i in range(0, 5):
    continue
    for j in range(0, 12):
        print(1 if any([(i, j, d) in dist for d in dirs])  else 0, end='')
    print()
print(min(dist.get(end, inf) for end in end_nodes))
# print the path
path = nx.shortest_path(graph2, source=start_nodes[0], target=end_nodes[0], weight='weight')
print(path)
# display the path in the grid
dir_map = {dirs[0]: '>', dirs[1]: '<', dirs[2]: '^', dirs[3]: 'v'}
for i in range(0, 5):
    for j in range(0, 12):
         for d in dirs:
             if (i, j, d) in path:
                 print(dir_map[d], end='')
                 break
         else:
             print('.', end='')
    print()


quit()

neighbors = set((i, j, d) 
                for n in start_nodes
                for i, j, d in graph2.neighbors(n))
print([n for n in neighbors]) # if (n[0], n[1]) in [(4,10)]])




quit()

start = (0, 0, dirs[0], 0)
end_nodes2 = [(max(i for i, j, *_ in g), max(j for i, j, *_ in g), dir, consec_steps)
                for consec_steps in range(0, 10)
                for dir in dirs]
dist2 = nx.single_source_dijkstra_path_length(graph2, source=start, weight='weight')
print(min(dist2.get(end, inf) for end in end_nodes2))



for i in range(0, 7):
    continue
    for j in range(0, 11):
        print(G[(i, j, dirs[0], 0)], end='')
    print()
print('-----------------')
# print the grid: 1 if reachable else 0   
for i in range(0, 5):
    for j in range(0, 12):
        print(1 if any([(i, j, d, c) in dist2 
                        for c in range(0, 10)
                        for d in dirs])  else 0, end='')
    print()

end_test = [(4, 11, d, c) 
            for c in range(0, 10)
            for d in dirs]
print(min(dist2.get(end, inf) for end in end_test))

# print all the neighbors for a given node set
neighbors = set((i, j, d, c) 
                for n in end_test 
                for i, j, d, c in graph2.neighbors(n))
print([n for n in neighbors if (n[0], n[1]) in [(4,10)]])


#print(end_nodes2)
