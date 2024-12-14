grid = {(x, y): int(val) for y, line in enumerate(open('2022/08/input.txt')) for x, val in enumerate(line.strip())}
height = max(y for x, y in grid) + 1
width = max(x for x, y in grid) + 1


# tree is visible if all trees in the grid to the (left, right, up, down) are shorter
def is_visible(x, y):
    cur_height = grid[(x, y)]
    if not any(grid.get((x-i, y), 0) >= cur_height for i in range(1, x+1)):
        return True
    if not any(grid.get((x+i, y), 0) >= cur_height for i in range(1, width-x)):
        return True
    if not any(grid.get((x, y-i), 0) >= cur_height for i in range(1, y+1)):
        return True
    if not any(grid.get((x, y+i), 0) >= cur_height for i in range(1, height-y)):
        return True
    return False

def scenic_score(x, y):
    seen_left = seen_right = seen_up = seen_down = 0
    for i in range(1, x+1):
        seen_left += 1
        if grid.get((x-i, y), 0) >= grid[(x, y)]: break
    for i in range(1, width-x):
        seen_right += 1
        if grid.get((x+i, y), 0) >= grid[(x, y)]: break
    for i in range(1, y+1):
        seen_up += 1
        if grid.get((x, y-i), 0) >= grid[(x, y)]: break
    for i in range(1, height-y):
        seen_down += 1
        if grid.get((x, y+i), 0) >= grid[(x, y)]: break
    return seen_right * seen_left * seen_up * seen_down

def print_grid(grid):
    for y in range(height):
        row = ''
        for x in range(width):
            if is_visible(x, y):
                row += f'\033[92m{str(grid[(x, y)])}\033[0m'  # Highlight visible trees in green
            else:
                row += str(grid[(x, y)])
        print(row)

def print_scenic_score(grid):
    max_score = max(scenic_score(x, y) for x, y in grid)
    for y in range(height):
        row = ''
        for x in range(width):
            score = scenic_score(x, y)
            val = grid[(x, y)]
            if score == 0:
                color = '\033[0m'  # Default color for zero scores
            else:
                # Scale the color intensity based on the score
                intensity = min(255, int(255 * (score / max_score)))
                color = f'\033[38;2;{intensity};0;0m'  # Red color with varying intensity
            row += f'{color}{str(val)}\033[0m'
        print(row)


print_grid(grid)
print_scenic_score(grid)
print()

print('part 1:', sum(1 for x, y in grid if is_visible(x, y)))
print('part 2:', max(scenic_score(x, y) for x, y in grid))