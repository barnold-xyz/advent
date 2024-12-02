import numpy as np

#data = np.loadtxt("2024/02/input.txt", dtype=int)
with open("2024/02/input.txt") as f:
    data = [list(map(int, line.split())) for line in f]

def validate(line):
    diffs = np.diff(line)
    abs_valid = all((np.abs(diffs) >= 1) & (np.abs(diffs) <= 3))
    sign_valid = len(set(np.sign(diffs))) == 1
    return abs_valid and sign_valid

def validate_pt2(line):
    if validate(line): return True
    # try removing one element at a time
    for i in range(len(line)):
        if validate(line[:i] + line[i+1:]): return True
    return False

print(sum([validate(line) for line in data]))
print(sum([validate_pt2(line) for line in data]))
