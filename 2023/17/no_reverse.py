import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

G = {(i, j, dir): int(c) for dir in dirs 
     for i, r in enumerate(open('2023/17/test.txt'))
     for j, c in enumerate(r.strip())}
g = list(G.keys())

graph = nx.DiGraph()
graph.add_nodes_from(g)
print('graph has nodes:', len(graph.nodes()))
nodes1 = graph.nodes()
print(graph)
for (i, j, dir) in g:
    for di, dj in dirs:
        if (di, dj) == (-dir[0], -dir[1]): continue
        neighbor = (i + di, j + dj, (di, dj))
        if neighbor in g:
            graph.add_edge((i, j, dir), neighbor, weight=G[neighbor])
print(graph)

start = (0, 0, dirs[0])
end_nodes = [(max(i for i, j, dir in g), max(j for i, j, dir in g), dir) for dir in dirs]
# find the distance from start to every other node
dist = nx.single_source_dijkstra_path_length(graph, source=start, weight='weight')

# find the dist to any end node
print([dist.get(end) for end in end_nodes])

quit()

# Visualize the graph in 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Position nodes based on their coordinates
pos = {node: (node[0], node[1], dirs.index(node[2])) for node in graph.nodes()}

# Draw nodes
for node, (x, y, z) in pos.items():
    ax.scatter(x, y, z, color='lightblue', s=100)

# Draw edges
for u, v in graph.edges():
    x = [pos[u][0], pos[v][0]]
    y = [pos[u][1], pos[v][1]]
    z = [pos[u][2], pos[v][2]]
    ax.plot(x, y, z, color='black')

# Draw edge labels (weights)
edge_labels = {(u, v): d['weight'] for u, v, d in graph.edges(data=True)}
for (u, v), weight in edge_labels.items():
    x = (pos[u][0] + pos[v][0]) / 2
    y = (pos[u][1] + pos[v][1]) / 2
    z = (pos[u][2] + pos[v][2]) / 2
    ax.text(x, y, z, str(weight), color='red')

#plt.show()



plt.show()
