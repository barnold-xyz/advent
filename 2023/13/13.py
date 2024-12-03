data = [grid.split('\n') for grid in open("2023/13/input.txt").read().strip().split('\n\n')]

def compare_lists(l1, l2):
    min_len = min(len(l1), len(l2))
    for i in range(min_len):
        if l1[i] != l2[i]:
            return False
    return True

def find_reflection(grid):
    for i, row in enumerate(grid[1:], start=1):
        first_half = grid[:i][::-1]
        second_half = grid[i:]
        if compare_lists(first_half, second_half):
            return i
    return 0

def summarize_reflections(grid):
    transposed_grid = [''.join(row) for row in zip(*grid)]
    horiz_mirror = find_reflection(grid)
    vert_mirror = find_reflection(transposed_grid)
    return 100 * horiz_mirror + vert_mirror

def part2(grid):
    def check_reflection(grid, find_reflection_func, any_ok=False):
        original_mirror = find_reflection_func(grid)
        for x, row in enumerate(grid):
            #if x == 0: continue
            for y, char in enumerate(row):
                #if y == 0: continue
                new_grid = grid.copy()
                new_row = list(new_grid[x])
                new_row[y] = '.' if new_row[y] == '#' else '#'
                new_grid[x] = ''.join(new_row)
                new_mirror = find_reflection_func(new_grid)
                if any_ok and new_mirror:
                    return new_mirror
                if (new_mirror != original_mirror) and (x+y) and new_mirror:
                    #print(f'FOUND smudge at {x}, {y}, new mirror: {new_mirror}')
                    #print('\n'.join(['  '.join(pair) for pair in zip(grid, new_grid)]))
                    return new_mirror
        return 0

    horiz_mirror = check_reflection(grid, find_reflection)
    transposed_grid = [''.join(row) for row in zip(*grid)]
    vert_mirror = check_reflection(transposed_grid, find_reflection, not horiz_mirror)

    #print(horiz_mirror, vert_mirror)
    return 100 * horiz_mirror + vert_mirror

print(sum(summarize_reflections(grid) for grid in data))
print(sum(part2(grid) for grid in data))
#print(part2(data[3]))
#test = data[3]
#print(part2(test))
#test = [''.join(row) for row in zip(*test)]
#print(part2(test))