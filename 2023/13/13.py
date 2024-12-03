data = [grid.split('\n') for grid in open("2023/13/input.txt").read().strip().split('\n\n')]

def compare_lists(l1, l2):
    min_len = min(len(l1), len(l2))
    for i in range(min_len):
        if l1[i] != l2[i]:
            return False
    return True

def find_reflection(grid):
    for i, row in enumerate(grid[1:], start=1):
        first_half = grid[:i]
        first_half = first_half[::-1]
        second_half = grid[i:]
        if compare_lists(first_half, second_half): return i
    return 0

def summarize_reflections(grid):
    #transposed_grid = list(map(list, zip(*grid)))
    transposed_grid = [''.join(row) for row in zip(*grid)]
    horiz_mirror = find_reflection(grid)
    vert_mirror = find_reflection(transposed_grid)
    print(horiz_mirror, vert_mirror)
    return 100*horiz_mirror + vert_mirror

print(sum(summarize_reflections(grid) for grid in data))
#[summarize_reflections(grid) for grid in data]
#summarize_reflections(data[5])

def t(grid):
    return [''.join(row) for row in zip(*grid)]

#print('\n'.join(data[5]))
#print('\n'.join(t(data[5])))

def find_reflection2(grid):
    debug = False
    print(grid)
    for i, row in enumerate(grid):
        print(i, row)
        debug = i == 9
        for j, next_row in enumerate(grid[i+1:]):
            if debug: print(i, j, 'comparing', grid[i], grid[i+j+1])
            if grid[i] != grid[i+j+1]: break
            if j == len(grid) - i - 2: return i + 1
    return 0


def find_reflection3(grid):
    for i, row in enumerate(grid[1:], start=1):
        first_half = grid[:i]
        first_half = first_half[::-1]
        second_half = grid[i:]
        if compare_lists(first_half, second_half): return i
    return 0

#print(find_reflection3(data[0]))
#print([find_reflection3(grid) for grid in data])

            

#print(find_reflection(data[5])) 
#print(find_reflection2(t(data[5])))
#print('====')
#print('\n'.join(t(data[5])))