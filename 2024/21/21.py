import networkx as nx

codes = open('2024/21/test.txt').read().splitlines()

keypad = nx.Graph()
keypad.add_edges_from([
    (7, 8), (7 ,4), (8, 9), (8, 5), (9, 6), 
    (4, 5), (4, 1), (5, 2), (5, 6), (6, 3), 
    (1, 2), (2, 3), (2, 0), (3, 'A'), (0, 'A')
])
import matplotlib.pyplot as plt

arroyw = nx.Graph()
arroyw.add_edges_from([
    
])

nx.draw(keypad, with_labels=True)
plt.show()