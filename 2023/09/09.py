import numpy as np

data = np.loadtxt("2023/09/input.txt", dtype=int)

def recursive(d, debug=False):
    if debug: print(d)
    if set(d) == {0}: return 0
    return recursive(np.diff(d), debug) + d[-1]


print(sum([recursive(d) for d in data]))
#test = recursive(data[1], True)
#print(test)
#print(len(data[1]), len(np.diff(data[1])))