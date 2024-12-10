from collections import defaultdict

graph = {(row, col): int(cell) for row, line in enumerate(open("2024/10/input.txt").readlines()) for col, cell in enumerate(line.strip())}
trailheads = [(row, col) for row, col in graph if graph[(row, col)] == 0]

def explore_trail(trailhead):
    trail = [trailhead]
    endpoints = defaultdict(int)
    while trail:
        row, col = trail.pop()
        if graph[(row, col)] == 9:
            endpoints[(row, col)] += 1
        for d in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            new_row, new_col = row + d[0], col + d[1]
            if graph.get((new_row, new_col), '') == graph[(row, col)] + 1:
                trail.append((new_row, new_col))
    return endpoints

trail_info = [explore_trail(trailhead) for trailhead in trailheads]
print(sum(len(info) for info in trail_info))
print(sum(sum(info.values()) for info in trail_info))