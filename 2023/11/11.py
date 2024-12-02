import itertools

univ = open("2023/11/input.txt").read().strip()
univ = univ.replace('.', '0').replace('#', '1')
univ = [list(map(int, list(row))) for row in univ.split('\n')]

def transpose(matrix):
    return [list(row) for row in zip(*matrix)]

def expand_universe(univ, factor=1):
    new_rows = list(range(len(univ)))
    new_cols = list(range(len(univ[0])))
    for i, row in enumerate(univ):
        if sum(row) == 0:
            for j in range(i, len(new_rows)):
                new_rows[j] += factor
    for i, col in enumerate(transpose(univ)):
        if sum(col) == 0:
            for j in range(i, len(new_cols)):
                new_cols[j] += factor
    return new_rows, new_cols

def find_galaxies(univ):
    galaxies = []
    for r, row in enumerate(univ):
        for c, cell in enumerate(row):
            if cell == 1:
                galaxies.append((r, c))
    return [(i+1, galaxy) for i, galaxy in enumerate(galaxies)]

def shortest_path(g1, g2, row_map, col_map):
    return abs(row_map[g1[0]] - row_map[g2[0]]) + abs(col_map[g1[1]] - col_map[g2[1]])

galaxies = find_galaxies(univ)

rows_pt1, cols_pt1 = expand_universe(univ, 1)
rows_pt2, cols_pt2 = expand_universe(univ, 1000000-1)

print(sum(shortest_path(g1, g2, rows_pt1, cols_pt1) for (i1, g1), (i2, g2) in itertools.combinations(galaxies, 2)))
print(sum(shortest_path(g1, g2, rows_pt2, cols_pt2) for (i1, g1), (i2, g2) in itertools.combinations(galaxies, 2)))
