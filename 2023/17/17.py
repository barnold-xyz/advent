import networkx as nx
from math import inf

input_file = '2023/17/input.txt'
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
    for di, dj in set(dirs) - {(dir[0], dir[1]),(-dir[0], -dir[1])}: # force a turn but not a 180
        for dist in range(4, 11):
            neighbor = (i+di*dist, j+dj*dist, (di, dj))
            skipped_nodes = [(i+di*dd, j+dj*dd, (di, dj)) for dd in range(1, dist)]
            weight = sum(G[n] for n in skipped_nodes if n in g) + (G[neighbor] if neighbor in g else 0)
            graph2.add_edge((i, j, dir), neighbor, weight=weight)

print(graph2)
## add the starting node
start = (0, 0, (0, 0))
graph2.add_node(start)
for i in range(4, 11):
    wt = sum(G[(0, j, (0, 1))] for j in range(0, i))
    graph2.add_edge(start, (0, i, (0, 1)), weight=wt)
print(graph2)

end_nodes = [(max(i for i, j, *_ in g), max(j for i, j, *_ in g), dir) for dir in dirs]

dist = nx.single_source_dijkstra_path_length(graph2, source=start, weight='weight')

print(min(dist.get(end, inf) for end in end_nodes))

# print the path
path = nx.shortest_path(graph2, source=start, target=end_nodes[0], weight='weight')
print(path)

# print the weights of each edge in the path
#print([graph2[path[i]][path[i+1]]['weight'] for i in range(0, len(path)-1)])
#print(graph2.get_edge_data(path[-2], path[-1]))

'''
# display the path in the grid
dir_map = {dirs[0]: '>', dirs[1]: '<', dirs[2]: 'v', dirs[3]: '^'}
for i in range(0, end_nodes[0][0]+1):
    for j in range(0, end_nodes[0][1]+1):
         for d in dirs:
             if (i, j, d) in path:
                 print(dir_map[d], end='')
                 break
         else:
             print('.', end='')
    print()


quit()
'''