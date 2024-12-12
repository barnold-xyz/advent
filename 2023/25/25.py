import networkx as nx
import matplotlib.pyplot as plt

data = open("2023/25/input.txt").read().split('\n')

G = nx.Graph()

for line in data:
    node, *neighbors = line.replace(':', '').split(' ')
    G.add_node(node)
    for neighbor in neighbors:
        G.add_edge(node, neighbor)

# Draw the original graph
#nx.draw(G, with_labels=True, font_size=6)
#plt.show()

# Remove specified edges
G.remove_edge('hgk', 'pgz')
G.remove_edge('lmj', 'xgs')
G.remove_edge('gzr', 'qnz')

# Find and draw each connected component
components = list(nx.connected_components(G))
print(len(components))
print(len(components[0]) * len(components[1]))
