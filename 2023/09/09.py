import numpy as np

data = np.loadtxt("2023/09/input.txt", dtype=int)

def recursive(d, part2=False, debug=False):
    if debug: print(d)
    if set(d) == {0}: return 0
    if part2: 
        return d[0] - recursive(np.diff(d), part2, debug) # doesn't work
    else:
        return recursive(np.diff(d), part2, debug) + d[-1]

#print(sum([recursive(d) for d in data]))

print(sum([recursive(d) for d in data]))
print(sum([recursive(d[::-1]) for d in data]))


