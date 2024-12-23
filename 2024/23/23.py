import networkx as nx

G = nx.Graph()
G.add_edges_from([tuple(line.strip().split('-')) for line in open('2024/23/input.txt')])

cliques = list(nx.enumerate_all_cliques(G))
print('part 1:', len([c for c in cliques if len(c) == 3 and any(node.startswith('t') for node in c)]))
print('part 2:', ','.join(sorted(max(cliques, key=len))))
