import random


grid = {(x, y): c for y, line in enumerate(open('2024/12/input.txt')) for x, c in enumerate(line.strip())}

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
def find_regions(grid):
    regions = []
    visited = set()
    for (x, y), value in grid.items():
        if (x, y) not in visited:
            region = set()
            stack = [(x, y)]
            while stack:
                cx, cy = stack.pop()
                if (cx, cy) in region:
                    continue
                region.add((cx, cy))
                visited.add((cx, cy))
                for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                    nx, ny = cx + dx, cy + dy
                    if (nx, ny) in grid and grid[(nx, ny)] == value and (nx, ny) not in visited:
                        stack.append((nx, ny))
            regions.append(region)
    return regions

def fence_cost(region):
    area = find_area(region)
    perimiter = find_perimeter(region)
    return area * perimiter

regions = find_regions(grid)
print(regions)
print_grid(grid, regions)
print(sum(fence_cost(region) for region in regions))