from concurrent.futures import ThreadPoolExecutor

# Load and process input
bricks = {chr(65 + i): tuple(map(int, line.replace('~', ',').split(','))) for i, line in enumerate(open("2023/22/input.txt").read().split('\n'))}
max_x = max(bricks.values(), key=lambda x: x[3])[3]
max_y = max(bricks.values(), key=lambda x: x[4])[4]
max_z = max(bricks.values(), key=lambda x: x[5])[5]

# Ensure coordinates are in order
for b in bricks:
    (sx, sy, sz, ex, ey, ez) = bricks[b]
    if sx > ex or sy > ey or sz > ez:
        print(f'UGH: {b}')
        quit()

# Print functions
def print_xz(bricks):
    for z in range(max_z, 0, -1):
        for x in range(max_x + 1):
            for brick, (sx, sy, sz, ex, ey, ez) in bricks.items():
                if sx <= x <= ex and sz <= z <= ez:
                    print(brick, end='')
                    break
            else:
                print('.', end='')
        print(f'\tz={z}')


def print_yz(bricks):
    for z in range(max_z, 0, -1):
        for y in range(max_y + 1):
            for brick, (sx, sy, sz, ex, ey, ez) in bricks.items():
                if sy <= y <= ey and sz <= z <= ez:
                    print(brick, end='')
                    break
            else:
                print('.', end='')
        print(f'\tz={z}')


def print_both(bricks):
    print_xz(bricks)
    print()
    print_yz(bricks)
    [print(f'{b}: {bricks[b]} supported by {find_supports(b, bricks)}') for b in bricks]
    print()

# Intersection check
def intersects(b1_coords, b2_coords):
    (sx1, sy1, sz1, ex1, ey1, ez1) = b1_coords
    (sx2, sy2, sz2, ex2, ey2, ez2) = b2_coords
    return not (ex1 < sx2 or ex2 < sx1 or ey1 < sy2 or ey2 < sy1 or ez1 < sz2 or ez2 < sz1)

# Find supports
def find_supports(brick, bricks):
    (sx, sy, sz, ex, ey, ez) = bricks[brick]
    test_sz = sz - 1
    test_ez = ez - 1
    supporting_bricks = []
    for brick2, coords in bricks.items():
        if brick2 != brick and intersects((sx, sy, test_sz, ex, ey, test_ez), coords):
            supporting_bricks.append(brick2)
    return supporting_bricks

# Fall logic
def fall_max(b, bricks):
    fell = False
    while True:
        (sx, sy, sz, ex, ey, ez) = bricks[b]
        if sz == 1 or ez == 1:
            break
        supporting_bricks = find_supports(b, bricks)
        if len(supporting_bricks) == 0:
            bricks[b] = (sx, sy, sz - 1, ex, ey, ez - 1)
            fell = True
        else:
            break
    return bricks, fell


def fall_all(bricks):
    fell = True
    while fell:
        for b in bricks:
            bricks, fell = fall_max(b, bricks)
    return bricks, fell

def fall_any(bricks):
    fell = True
    while fell:
        fell = False
        for b in list(bricks.keys()):
            _, has_fallen = fall_max(b, bricks)
            if has_fallen:
                fell = True
                return True
    return fell

# Check if a brick can disintegrate
def can_disintegrate(b, bricks):
    test_bricks = bricks.copy()
    del test_bricks[b]
    return fall_all(test_bricks.copy())[0] == test_bricks

# Find all supports
def find_all_supports(bricks):
    return {b: find_supports(b, bricks) for b in bricks}

# Wrapper for parallel execution
def can_disintegrate_parallel(b):
    print(f'Checking brick {b}')
    test_bricks = bricks.copy()
    del test_bricks[b]
    return not fall_any(test_bricks)

# Main program
print("Dropping bricks")
bricks, _ = fall_all(bricks)

print("Finding supports")
supports = find_all_supports(bricks)

print("Disintegrating bricks")
with ThreadPoolExecutor() as executor:
    dis = list(executor.map(can_disintegrate_parallel, bricks.keys()))

print(sum(dis))
