import itertools, numpy as np, re

loc_x = {
    '7': 0, '8': 0, '9': 0,
    '4': 1, '5': 1, '6': 1,
    '1': 2, '2': 2, '3': 2,
    '#': 3, '^': 3, 'A': 3,
    '<': 4, 'v': 4, '>': 4,
}

loc_y = {
    '7': 0, '8': 1, '9': 2,
    '4': 0, '5': 1, '6': 2,
    '1': 0, '2': 1, '3': 2,
    '#': 0, '^': 1, 'A': 2,
    '<': 0, 'v': 1, '>': 2,
}

def bestPath(x1, y1, x2, y2):
    lt, rt = '<' * (y1 - y2), '>' * (y2 - y1)
    up, dn = '^' * (x1 - x2), 'v' * (x2 - x1)
    if loc_x['#'] == min(x1, x2) and loc_y['#'] == min(y1, y2):
        return dn + rt + up + lt + "A"
    elif loc_x['#'] == max(x1, x2) and loc_y['#'] == min(y1, y2):
        return up + rt + dn + lt + "A"
    else:
        return lt + dn + up + rt + "A"

options = 'A^<v>'
pairs = [x+y for (x,y) in itertools.product(options, options)]
N = len(pairs)
matrix = np.array([[0 for i in range(N)] for j in range(N)], dtype=object)

for srcidx, pair in enumerate(pairs):
    a,b = pair[0],pair[1]
    path = bestPath(loc_x[a], loc_y[a], loc_x[b], loc_y[b])
    for (c1, c2) in zip('A'+path, path):
        matrix[srcidx, pairs.index(c1+c2)] += 1

def fastestPairs(depth):
    vect = np.array([1]*N, dtype=object)
    return np.linalg.matrix_power(matrix,depth).dot(vect)

def fastestStr(str, fp):
    return sum(fp[pairs.index(a+b)] for (a,b) in zip("A" + str, str))

def solveStr(str, depth):
    str = str.replace('0', '^')
    if (depth == 0): return len(str)
    fp = fastestPairs(depth - 1)
    result = 0
    for (c1, c2) in zip("A" + str, str):
        result += fastestStr(bestPath(loc_x[c1], loc_y[c1], loc_x[c2], loc_y[c2]), fp)
    return result

text = open("2024/21/input.txt").read()

def solve(depth):
    result = 0
    for code in text.splitlines():
        fastest = solveStr(code, depth)
        result += fastest * int(re.findall(r'\d+', code)[0])
    return result

print(solve(3))
print(solve(26))
print(solveStr('3141592653589793238462643383279502A', 10000))
