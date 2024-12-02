import itertools

univ = open("2023/11/test.txt").read().strip()
univ = univ.replace('.', '0').replace('#', '1')
univ = [list(map(int, list(row))) for row in univ.split('\n')]

def transpose(matrix):
    return [list(row) for row in zip(*matrix)]

def expand_universe(univ):
    expanded_rows = []
    expanded_universe = []
    for row in univ:
        if(sum(row) == 0): expanded_rows.append(row)
        expanded_rows.append(row)
    for col in transpose(expanded_rows):
        if(sum(col) == 0): expanded_universe.append(col)
        expanded_universe.append(col)
    return transpose(expanded_universe)

def univ_to_str(univ):
    return '\n'.join([''.join(map(str, row)) for row in univ])

def find_galaxies(univ):
    galaxies = []
    for r, row in enumerate(univ):
        for c, cell in enumerate(row):
            if cell == 1:
                galaxies.append((r, c))
    return [(i+1, galaxy) for i, galaxy in enumerate(galaxies)]

def shortest_path(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

#print(univ)
#print("\n")
expanded_univ = expand_universe(univ)
#print(univ_to_str(expanded_univ))
#print("\n")

galaxies = find_galaxies(expanded_univ)
#print("Galaxies:", galaxies)

# Iterate through all pairs of galaxies
#for (i1, g1), (i2, g2) in itertools.combinations(galaxies, 2):
#    print(f"Pair: Galaxy {i1} at {g1} and Galaxy {i2} at {g2}, Shortest Path: {shortest_path(g1[0], g1[1], g2[0], g2[1])}")
print(sum([shortest_path(g1[0], g1[1], g2[0], g2[1]) for (i1, g1), (i2, g2) in itertools.combinations(galaxies, 2)]))