import itertools

grid = {(x, y): char for y, line in enumerate(open("2024/08/input.txt").read().split('\n')) for x, char in enumerate(line)}
width = max(x for x, y in grid.keys()) + 1
height = max(y for x, y in grid.keys()) + 1

def print_grid(grid, antinodes=set()):
    print()
    for y in range(width):
        for x in range(height):
            if (x, y) in antinodes:
                print('X', end='')
            else:
                print(grid.get((x, y), '.'), end='')
        print()
    print()


antinodes = set()
def add_antinodes(source1, source2):
    xdiff = source2[0] - source1[0]
    ydiff = source2[1] - source1[1]
    #print(f'source1: {source1}, source2: {source2}')
    #print(f'xdiff: {xdiff}, ydiff: {ydiff}')
    anti1 = (source1[0] - xdiff, source1[1] - ydiff)
    anti2 = (source2[0] + xdiff, source2[1] + ydiff)
    #print(f'anti1: {anti1}, anti2: {anti2}')
    if anti1 in grid: antinodes.add(anti1)
    if anti2 in grid: antinodes.add(anti2) 

antinodes_pt2 = set()
def add_antinodes_pt2(source1, source2):
    xdiff = source2[0] - source1[0]
    ydiff = source2[1] - source1[1]

    # start at source1 and move right until the end of the grid
    for i in range(0, width):
        node = (source1[0] + i*xdiff, source1[1] + i*ydiff)
        if node in grid: 
            antinodes_pt2.add(node)
        else: 
            break
    # now move left until the end of the grid
    for i in range(0, width):
        node = (source1[0] - i*xdiff, source1[1] - i*ydiff)
        if node in grid: 
            antinodes_pt2.add(node)
        else: 
            break

# find all pairs of nodes that have the same grid value
def find_pairs(grid):
    antenna_loc = {char: [pos for pos, c in grid.items() if c == char] for char in set(grid.values()) if char != '.'}
    pairs = {char: list(itertools.combinations(locs, 2)) for char, locs in antenna_loc.items()}
    #print(antenna_loc)
    #print(pairs)
    return pairs

def add_all_antinodes(grid, fn=add_antinodes):
    pairs = find_pairs(grid)
    for char, locs in pairs.items():
        for loc1, loc2 in locs:
            fn(loc1, loc2)

#print(grid)
#print_grid(grid)
add_all_antinodes(grid)
#print_grid(grid, antinodes)
print(len(antinodes))
add_all_antinodes(grid, fn=add_antinodes_pt2)
print(len(antinodes_pt2))
#print_grid(grid, antinodes_pt2)