bricks = {chr(65+i): tuple(map(int, line.replace('~',',').split(','))) for i, line in enumerate(open("2023/22/input.txt").read().split('\n'))}
max_x = max(bricks.values(), key=lambda x: x[3])[3]
max_y = max(bricks.values(), key=lambda x: x[4])[4]
max_z = max(bricks.values(), key=lambda x: x[5])[5]

# check that the coords are in order
for b in bricks:
    (sx, sy, sz, ex, ey, ez) = bricks[b]
    if sx > ex or sy > ey or sz > ez:
        print(f'UGH: {b}')
        quit()

# print the view that shows the x and z axes. blank = '.', brick = 'A'-'Z'
def print_xz(bricks):
    for z in range(max_z, 0, -1):
        for x in range(max_x+1):
            for brick, (sx, sy, sz, ex, ey, ez) in bricks.items():
                if sx <= x <= ex and sz <= z <= ez:
                    print(brick, end='')
                    break
            else:
                print('.', end='')
        print(f'\tz={z}')

def print_yz(bricks):
    for z in range(max_z, 0, -1):
        for y in range(max_y+1):
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

# return True if the two bricks intersect
def intersects(b1_coords, b2_coords):
    (sx1, sy1, sz1, ex1, ey1, ez1) = b1_coords
    (sx2, sy2, sz2, ex2, ey2, ez2) = b2_coords
    return not (ex1 < sx2 or ex2 < sx1 or ey1 < sy2 or ey2 < sy1 or ez1 < sz2 or ez2 < sz1)

# returns a list of the bricks that support the given brick
def find_supports(brick, bricks):
    (sx, sy, sz, ex, ey, ez) = bricks[brick]
    test_sz = sz - 1
    test_ez = ez - 1
    supporting_bricks = []
    for brick2, coords in bricks.items():
        if brick2 != brick and intersects((sx, sy, test_sz, ex, ey, test_ez), coords):
            supporting_bricks.append(brick2)
    return supporting_bricks

def fall_max(b, bricks):
    fell = False
    while True:
        (sx, sy, sz, ex, ey, ez) = bricks[b]
        if sz == 1 or ez == 1:
            break
        supporting_bricks = find_supports(b, bricks)
        #print(f'{b}:\t{bricks[b]}\tsupported by:{supporting_bricks}')
        if len(supporting_bricks) == 0:
            bricks[b] = (sx, sy, sz-1, ex, ey, ez-1)
            fell = True
        else:
            break
    return bricks, fell

def fall_all(bricks):
    num_fell = 0
    while True:
        can_fall = []
        for b in sorted(bricks, key=lambda x: bricks[x][2], reverse=True):
            (sx, sy, sz, ex, ey, ez) = bricks[b]
            if sz > 1 and ez > 1:
                supporting_bricks = find_supports(b, bricks)
                if len(supporting_bricks) == 0:
                    can_fall.append(b)
        
        if not can_fall:
            break
        
        for b in can_fall:
            (sx, sy, sz, ex, ey, ez) = bricks[b]
            bricks[b] = (sx, sy, sz-1, ex, ey, ez-1)
        num_fell += len(can_fall) 
    
    return bricks, bool(can_fall), num_fell

# returns True if nothing falls after the brick is removed
def can_disintegrate(b, bricks):
    test_bricks = bricks.copy()
    del test_bricks[b]
    return fall_all(test_bricks.copy())[0] == test_bricks

def find_all_supports(bricks):
    return {b: find_supports(b, bricks) for b in bricks}

def can_disintegrate2(b, supports):
    dependents = [d for d in supports if supports[d]==[b]]
    print(f'dependents for {b}: {dependents}')
    return len(dependents) == 0

# how many bricks will fall if the given brick is removed
# strategy: remove the brick, then check how many bricks can fall
# but only remove 1 brick at a time
def chain_reaction(bricks, supports):
    fell = {}
    for b in bricks:
        disintegrated = set(b)
        fell[b] = []
        while True:
            new_disintegrated = [d for d in bricks if (not d in disintegrated) and set(supports[d]) in disintegrated]
            if not new_disintegrated:
                break
            print(f'{disintegrated} disintegrated, {new_disintegrated} fell')
            disintegrated.update(new_disintegrated)
        fell[b].append(disintegrated)

    return fell


#print_both(bricks)
print('dropping bricks')
bricks, *_ = fall_all(bricks)
#print_both(bricks)
print('finding supports')
supports = find_all_supports(bricks)


print("disintegrating bricks")
#dis = [can_disintegrate(b, bricks.copy()) for b in list(bricks.keys())]
#print(sum(dis))
dis2 = {b:can_disintegrate2(b, supports) for b in bricks}
print(dis2)
print(sum(dis2.values()))
rxn = chain_reaction(bricks, supports)
print(sum(len(r) for r in rxn.values()))


#print(sum(can_disintegrate(b, bricks) for b in bricks))
#[print(f'{b}: {find_supports(b, bricks)}') for b in bricks]