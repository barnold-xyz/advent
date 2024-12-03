data = open("2023/14/input.txt").read().strip().split('\n')

def transpose(data):
    return [''.join(row) for row in zip(*data)]
#print('\n'.join(data))

#flipped = [''.join(row) for row in zip(*data)]
flipped = transpose(data)
#print('\n\n')
#print('\n'.join(flipped))

# every zero rolls to the left until it hits the end, another 0, or a #, then stops
def roll_left(row):
    groups = row.split('#')
    new_row = '#'.join([''.join(sorted(g, reverse=True)) for g in groups])
    return new_row

def score(data):
    return sum((len(data) - i) * row.count('O') for i, row in enumerate(data))

rolled = transpose([roll_left(row) for row in transpose(data)])
print('\n'.join(rolled))
print(score(rolled))