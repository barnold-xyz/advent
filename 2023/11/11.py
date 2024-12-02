import itertools

# Read and process the input data
univ = open("2023/11/input.txt").read().strip()
univ = univ.replace('.', '0').replace('#', '1')
univ = [list(map(int, list(row))) for row in univ.split('\n')]

def transpose(matrix):
    return [list(row) for row in zip(*matrix)]

# Insert 'factor' number of rows/cols in place of any rows/cols that are all 0
def expand_universe(univ, factor=1):
    row_adj = list(itertools.accumulate([factor * (sum(row) == 0) for row in univ]))
    col_adj = list(itertools.accumulate([factor * (sum(col) == 0) for col in transpose(univ)]))
    return row_adj, col_adj

def find_galaxies(univ):
    return [(i+1, (r, c)) for i, (r, row) in enumerate(enumerate(univ)) for c, cell in enumerate(row) if cell == 1]

def shortest_path(g1, g2, row_adj, col_adj):
    x1, y1 = g1
    x2, y2 = g2
    xdiff = abs((x1 + row_adj[x1]) - (x2 + row_adj[x2]))
    ydiff = abs((y1 + col_adj[y1]) - (y2 + col_adj[y2]))
    return xdiff + ydiff

galaxies = find_galaxies(univ)

rows_pt1, cols_pt1 = expand_universe(univ, 1)
rows_pt2, cols_pt2 = expand_universe(univ, 1000000-1)

print(sum(shortest_path(g1, g2, rows_pt1, cols_pt1) for (i1, g1), (i2, g2) in itertools.combinations(galaxies, 2)))
print(sum(shortest_path(g1, g2, rows_pt2, cols_pt2) for (i1, g1), (i2, g2) in itertools.combinations(galaxies, 2)))