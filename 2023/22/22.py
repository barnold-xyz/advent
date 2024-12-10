bricks = [line.replace('~',',').split(',') for line in open("2023/22/test.txt").read().split('\n')]
bricks = [list(map(int, brick)) for brick in bricks]

# quick check
for brick in bricks:
    if brick[0] > brick[3] or brick[1] > brick[4] or brick[2] > brick[5]:
        print(f'UGH: {brick}')

def fall_once(bricks):
    moved = False
    for brick in bricks:
        (sx, sy, sz, ex, ey, ez) = brick
        if(sz == 1 or ez == 1):
            continue
        supporting_bricks = find_supports(brick, bricks)
        if len(supporting_bricks) == 0:
            brick[2] -= 1
            brick[5] -= 1
            moved = True
            break
        else:
            #print(f'brick: {brick}, supporting bricks: {supporting_bricks}')
            pass
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
            if ((sx2 >= sx and sx2 <= ex) or (ex2 >= sx and ex2 <= ex)) and \
                ((sy2 >= sy and sy2 <= ey) or (ey2 >= sy and ey <= ey)):
                supporting_bricks.append(brick2)
    return supporting_bricks

def find_all_supports(bricks):
    brick_to_supporters = {}
    for brick in bricks:
        brick_to_supporters[tuple(brick)] = find_supports(brick, bricks)
    return brick_to_supporters

[print(brick) for brick in bricks]
print('............')
bricks2 = fall_all(bricks.copy())
[print(brick) for brick in bricks2]
print('............')
supports = find_all_supports(bricks2)
[print(f'{brick}: {supporters}') for brick, supporters in supports.items()]
print('............')

# looking for the bricks that are the sole support for another brick
def find_sole_supports(bricks, supports):
    sole_supports = []
    for brick, supporters in supports.items():
        if len(supporters) == 1:
            sole_supports.append(brick)
    return sole_supports

sole_supports = find_sole_supports(bricks2, supports)
print(f'sole supports: {sole_supports}')
print(f'len bricks: {len(bricks2)}, len sole supports: {len(sole_supports)}')
