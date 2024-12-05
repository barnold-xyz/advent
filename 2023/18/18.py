import matplotlib.pyplot as plt

# Read and process the data
data = [line.split(' ') for line in open('2023/18/test.txt').read().split('\n')]

edges = []
i = j = 0
dir_map = dict(zip('RLUD', [(0, 1), (0, -1), (-1, 0), (1, 0)]))
for dir_code, length, color in data:
    dir = dir_map[dir_code]
    edges.append({
        'start': (i, j), 
        'end': (i + int(length) * dir[0], j + int(length) * dir[1]),
        'color': color        
    })
    i += int(length) * dir[0]
    j += int(length) * dir[1]

print(edges)

# Plot the edges
plt.figure(figsize=(8, 8))
for edge in edges:
    start = edge['start']
    end = edge['end']
    color = 'red' #edge['color']
    plt.plot([start[1], end[1]], [start[0], end[0]], color=color, linewidth=2)

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Edges Plot')
plt.grid(True)
plt.gca().invert_yaxis()  # Invert Y-axis to match the coordinate system used in the data
plt.show()
