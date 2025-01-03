from functools import lru_cache

data = open("2023/14/input.txt").read().strip().split('\n')

def transpose(data):
    return [''.join(row) for row in zip(*data)]

def rotate(data):
    return [''.join(row) for row in zip(*data)][::-1]

# every zero rolls to the left until it hits the end, another 0, or a #, then stops
def roll(row, left=True):
    groups = row.split('#')
    new_row = '#'.join([''.join(sorted(g, reverse=left)) for g in groups])
    return new_row

def score(data):
    return sum((len(data) - i) * row.count('O') for i, row in enumerate(data))

rolled = transpose([roll(row) for row in transpose(data)])
#print('\n'.join(rolled))
print(score(rolled))

@lru_cache(maxsize=None)
def cycle(data):
    # Convert data to a tuple of strings for caching
    #data = tuple(data)
    
    # north
    data = transpose([roll(row) for row in transpose(data)])
    #print('north')
    #print('\n'.join(data))

    # west
    data = [roll(row) for row in data]
    #print('west')
    #print('\n'.join(data))

    # south
    data = transpose([roll(row, left=False) for row in transpose(data)])
    #print('south')
    #print('\n'.join(data))

    # east
    data = [roll(row, left=False) for row in data]
    #print('east')
    #print('\n'.join(data))

    return tuple(data)

# Convert data to a tuple of strings for caching
data = tuple(data)

for i in range(1000000000):
    data = cycle(data)
    if i % 1000000 == 0:
        print(i, i/1000000000)
    #new_data = cycle(data)
    #if new_data == data:
    #    print('repeated after', i)
    #    break
    #data = new_data

print(score(data))