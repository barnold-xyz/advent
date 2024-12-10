
graph = {(row, col): int(cell) for row, line in enumerate(open("2024/10/input.txt").readlines()) for col, cell in enumerate(line.strip())}
trailheads = [(row, col) for row, col in graph if graph[(row, col)] == 0]

#print(graph)
#print(trailheads)

def explore_trail(trailhead):
    trail = [trailhead]
    endpoints = set()
    while trail:
        row, col = trail.pop()
        if graph[(row, col)] == 9:
            print(f'reached end! {row, col}')
            endpoints.add((row, col))
        for d in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            new_row, new_col = row + d[0], col + d[1]
            if graph.get((new_row, new_col), '') == graph[(row, col)] + 1:
                #print('moving to', new_row, new_col, graph[(new_row, new_col)])
                trail.append((new_row, new_col))
    return endpoints

print(sum(len(explore_trail(trailhead)) for trailhead in trailheads))

