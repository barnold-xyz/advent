import random
import matplotlib.pyplot as plt


grid = {(x, y): c for y, line in enumerate(open('2024/12/input.txt')) for x, c in enumerate(line.strip())}
height = max(y for x, y in grid) + 1
width = max(x for x, y in grid) + 1

def print_grid(grid, regions=[]):
    colors = ['\033[38;5;{}m'.format(i) for i in range(16, 232)]
    random.shuffle(colors)
    color_map = {}
    for idx, region in enumerate(regions):
        color = colors[idx % len(colors)]
        for cell in region:
            color_map[cell] = color

    for y in range(max(y for x, y in grid) + 1):
        for x in range(max(x for x, y in grid) + 1):
            if (x, y) in color_map:
                print(color_map[(x, y)] + grid.get((x, y), ' ') + '\033[0m', end='')
            else:
                print(grid.get((x, y), ' '), end='')
        print()
    

def find_area(region):
    return len(region)

# region is a set of contiguous unit squares
def find_perimeter(region):
    perimeter = 0
    for x, y in region:
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            if (x + dx, y + dy) not in region:
                perimeter += 1
    return perimeter

# returns a list of contiguous regions of unit squares
# regions are a set of (x, y) blocks and a set of (x1, y1), (x2, y2) edges
def find_regions(grid):
    regions = []
    visited = set()
    for (x, y), value in grid.items():
        if (x, y) not in visited:
            blocks = set()
            edges = []
            stack = [(x, y)]
            while stack:
                cx, cy = stack.pop()
                if (cx, cy) in blocks:
                    continue
                blocks.add((cx, cy))
                edge_top = {(cx, cy), (cx+1, cy)}
                edge_right = {(cx+1, cy), (cx+1, cy+1)}
                edge_bot = {(cx+1, cy+1), (cx, cy+1)}
                edge_left = {(cx, cy+1), (cx, cy)}
                for e in [edge_top, edge_right, edge_bot, edge_left]:
                    if not e in edges:
                        edges.append(e)
                if (cx+1, cy) in blocks: # block to the right is already in, so remove the edge since it's interior
                    edges.remove(edge_right)
                if (cx, cy+1) in blocks: # block below
                    edges.remove(edge_bot)
                if (cx-1, cy) in blocks: # block to the left
                    edges.remove(edge_left)
                if (cx, cy-1) in blocks: # block above
                    edges.remove(edge_top)

                visited.add((cx, cy))
                for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                    nx, ny = cx + dx, cy + dy
                    if (nx, ny) in grid and grid[(nx, ny)] == value and (nx, ny) not in visited:
                        stack.append((nx, ny))
            region = {'blocks': blocks, 'edges': edges}
            regions.append(region)
    return regions

def scan_for_sides(region):
    blocks = region['blocks']
    sides = 0
    # start scanning top to bottom, looking for cells with nothing above them or below them
    for y in range(height):
        none_above = []
        none_below = []
        for x in range(width):
            if (x, y) in blocks:
                if (x, y-1) not in blocks:
                    none_above.append((x, y))
                if (x, y+1) not in blocks:
                    none_below.append((x, y))
        # now check if the cells in none_above and none_below are contiguous
        # print(f'none_above: {none_above}')
        # print(f'none_below: {none_below}')
        sides_above = 1 if none_above else 0
        for i in range(1, len(none_above)):
            if none_above[i][0] != none_above[i-1][0] + 1:
                sides_above += 1
        sides_below = 1 if none_below else 0
        for i in range(1, len(none_below)):
            if none_below[i][0] != none_below[i-1][0] + 1:
                sides_below += 1
        # print(f'sides_above: {sides_above}, sides_below: {sides_below}')
        sides += sides_above + sides_below
        # print(f'sides: {sides}')

    # now scan left to right, looking for cells with nothing to the left or right of them
    for x in range(width):
        none_left = []
        none_right = []
        for y in range(height):
            if (x, y) in blocks:
                if (x-1, y) not in blocks:
                    none_left.append((x, y))
                if (x+1, y) not in blocks:
                    none_right.append((x, y))
        # now check if the cells in none_left and none_right are contiguous
        # print(f'none_left: {none_left}')
        # print(f'none_right: {none_right}')
        sides_left = 1 if none_left else 0
        for i in range(1, len(none_left)):
            if none_left[i][1] != none_left[i-1][1] + 1:
                sides_left += 1
        sides_right = 1 if none_right else 0
        for i in range(1, len(none_right)):
            if none_right[i][1] != none_right[i-1][1] + 1:
                sides_right += 1
        # print(f'sides_left: {sides_left}, sides_right: {sides_right}')
        sides += sides_left + sides_right
        # print(f'sides: {sides}')
    return sides

def score_part2(region):
    sides = scan_for_sides(region)
    area = find_area(region['blocks'])
    return area * sides


def fence_cost(region):
    area = find_area(region['blocks'])
    perimiter = find_perimeter(region['blocks'])
    return area * perimiter

def is_parallel(edge1, edge2):
    (x1, y1), (x2, y2) = edge1
    (x3, y3), (x4, y4) = edge2
    return (x2 - x1) * (y4 - y3) == (y2 - y1) * (x4 - x3)

def calc_perimeter_and_sides(region):
    edges = sorted(region['edges'])
    perim = len(edges)

    sides = 0
    next_edge = sorted(list(edges))[0]
    next_point = list(next_edge)[0]
    while edges:
        cur_edge = next_edge
        edges.remove(cur_edge)
        prev_point = next_point
        cur_point = next(p for p in cur_edge if p != prev_point)
        if prev_point == next_point:
            print(f"UHOH Previous point: {prev_point}, Current point: {cur_point}")
            prev_point, cur_point = cur_point, prev_point
        print(f"Previous point: {prev_point}, Current point: {cur_point}")
        next_edge = next((e for e in edges if cur_point in e), None)
        if next_edge is None:
            break
        print(f"Current edge: {cur_edge}, Next edge: {next_edge}")
        next_point = next(p for p in next_edge if p != cur_point)
        if is_parallel(cur_edge, next_edge):
            print(f'Edges {cur_edge} and {next_edge} are parallel')
            continue
        else:
            print(f'Edges {cur_edge} and {next_edge} are NOT parallel')
            sides += 1

    return perim, sides

def plot_edges(edges):
    print(edges)
    for (x1, y1), (x2, y2) in edges:
        plt.plot([x1, x2], [y1, y2], 'ro-')
    plt.show()

regions = find_regions(grid)
print(scan_for_sides(regions[0]))
print(sum(score_part2(r) for r in regions))
quit()

#print(regions)
print_grid(grid, [region['blocks'] for region in regions])
print(sum(fence_cost(region) for region in regions))

for r in regions:
    print('region:', next(grid[(x, y)] for x, y in r['blocks']))
    print(f'len blocks: {len(r["blocks"])}')
    print(f'len edges: {len(r["edges"])}')

print(regions[0]['blocks'])
print(regions[0]['edges'])

# Plot the edges of the regions
plot_edges(regions[0]['edges'])

# Calculate perimeter and sides for the first region
calc_perimeter_and_sides(regions[6])