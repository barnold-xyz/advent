import networkx as nx

G = {(i, j): int(c) for i, r in enumerate(open('2023/17/test_small.txt'))
     for j, c in enumerate(r.strip())}
g = list(G.keys())

graph = nx.DiGraph()
graph.add_nodes_from(g)

moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

for (i, j) in g:
    for di, dj in moves:
        neighbor = (i + di, j + dj)
        if neighbor in g:
            graph.add_edge((i, j), neighbor, weight=G[neighbor])

# Print the graph information
#print("Nodes:", graph.nodes())
#print("Edges:", graph.edges(data=True))

# Find the shortest path from the start to the end
start = (0,0)
end = (max(i for i, j in g), max(j for i, j in g))

path = nx.shortest_path(graph, source=start, target=end, weight='weight')
print(path)
path_length = nx.shortest_path_length(graph, source=start, target=end, weight='weight')
print(path_length)
