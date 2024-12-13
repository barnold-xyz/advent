pair_assignments = [list(map(int, pair.replace('-', ',').split(','))) for pair in open('2022/04/input.txt').read().strip().split('\n')]

def is_fully_overlapped(pair):
    return (pair[0] <= pair[2] and pair[1] >= pair[3]) or \
              (pair[0] >= pair[2] and pair[1] <= pair[3])

def any_overlap(pair):
    return pair[2] <= pair[0] <= pair[3] or pair[2] <= pair[1] <= pair[3] or \
              pair[0] <= pair[2] <= pair[1] or pair[0] <= pair[3] <= pair[1]

print('part 1: ', sum(is_fully_overlapped(pair) for pair in pair_assignments))
print('part 2: ', sum(any_overlap(pair) for pair in pair_assignments))
