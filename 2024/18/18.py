bytes = [(int(x), int(y)) for line in open("2024/18/input.txt").read().splitlines() 
         for x, y in [line.split(',')]]

height = width = 70+1

def print_grid(t, path=[]):
    for y in range(height):
        for x in range(width):
            if (x, y) in bytes[:t]:
                print('#', end='')
            elif (x, y) in path:
                print('O', end='')
            else:
                print('.', end='')
        print()

def dfs(start, end, t):
    stack = [(start, [start])]
    visited = set()
    while stack:
        (node, path) = stack.pop()
        if node == end:
            return path
        if node in visited:
            continue
        visited.add(node)
        x, y = node
        if x < 0 or x >= width or y < 0 or y >= height:
            continue
        if node in bytes[:t]:
            continue
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            stack.append(((x+dx, y+dy), path + [(x+dx, y+dy)]))
    return None

def bfs(start, end, t):
    queue = [(start, [start])]
    visited = set()
    while queue:
        (node, path) = queue.pop(0)
        if node == end:
            return path
        if node in visited:
            continue
        visited.add(node)
        x, y = node
        if x < 0 or x >= width or y < 0 or y >= height:
            continue
        if node in bytes[:t]:
            continue
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            queue.append(((x+dx, y+dy), path + [(x+dx, y+dy)]))
    return None

time = 1024
start = (0, 0)
end = (width-1, height-1)

path = bfs(start, end, time)
print('part 1:', len(path)-1)

for t in range(time, len(bytes)):
    if bytes[t] in path:
        path = bfs(start, end, t)
        if path is None:
            print(f'part 2: time: {t-1}, next byte: {bytes[t-1]}')
            # print_grid(t-1, dfs(start, end, t-1))
            break
