bricks = [line.replace('~',',').split(',') for line in open("2023/22/test.txt").read().split('\n')]
bricks = [list(map(int, brick)) for brick in bricks]

# quick check
for brick in bricks:
    if brick[0] > brick[3] or brick[1] > brick[4] or brick[2] > brick[5]:
        print(f'UGH: {brick}')

def fall_once(bricks):
    moved = False
    for brick in bricks:
        can_fall = True
        (sx, sy, sz, ex, ey, ez) = brick
        supporting_bricks = []
        if sz == 1 or ez == 1:  # bricks laying on the ground can't fall
            continue

        # check if there is a brick below, if not, move down
        # a brick is below if it's x- or y- coordinates are between the x- and y- coordinates of the brick and the brick is one level below
        for brick2 in bricks:
            (sx2, sy2, sz2, ex2, ey2, ez2) = brick2
            if ez2 == sz - 1: # brick2 is one level below brick, so it's a candidate
                if (sx2 >= sx and sx2 <= ex) or (ex2 >= sx and ex2 <= ex) or \
                    (sy2 >= sy and sy2 <= ey) or (ey2 >= sy and ey2 <= ey):
                    can_fall = False
                    supporting_bricks.append(brick2)
        if can_fall:
            brick[2] -= 1
            brick[5] -= 1
            moved = True
            break
        else:
            print(f'brick: {brick}, supporting bricks: {supporting_bricks}')
    return moved, bricks

def fall_all(bricks):
    moved = True
    while moved:
        moved, bricks = fall_once(bricks)
    return bricks


# for each brick, find the bricks that support it
def find_supports(brick, bricks): 
    (sx, sy, sz, ex, ey, ez) = brick
    supporting_bricks = []
    for brick2 in bricks:
        (sx2, sy2, sz2, ex2, ey2, ez2) = brick2
        if ez2 == sz - 1: # brick2 is one level below brick, so it's a candidate
            if (sx2 >= sx and sx2 <= ex) or (ex2 >= sx and ex2 <= ex) or \
                (sy2 >= sy and sy2 <= ey) or (ey2 >= sy and ey <= ey):
                supporting_bricks.append(brick2)
    return supporting_bricks

def find_all_supports(bricks):
    supports = {}
    for brick in bricks:
        supports[tuple(brick)] = find_supports(brick, bricks)
    return supports

def find_necessary_bricks(bricks, supports):
    return [li for li in supports.values() if li in bricks]

bricks = fall_all(bricks)
supports = find_all_supports(bricks)
temp = [support for support in supports.values() if len(support) == 1]
print(temp)