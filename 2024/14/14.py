import matplotlib.pyplot as plt
import imageio
from collections import Counter
import numpy as np
from math import prod, inf

file = "2024/14/input.txt"
data = [line for line in open(file).read().splitlines()]
data = [tuple(map(int, item.replace('p=', '').replace('v=', '').replace(' ', ',').split(','))) for item in data]

(height, width) = (103,101) if file.endswith("input.txt") else (7, 11)

def find_location(init, time, height=height, width=width):
    x, y, vx, vy = init
    return ((x + vx * time) % width, (y + vy * time) % height)

def print_grid(robots, height=height, width=width):
    robo_count = Counter(robots)
    for y in range(height):
        for x in range(width):
            if (x, y) in robo_count:
                print(robo_count[(x, y)], end='')
            else:
                print('.', end='')
        print()

def save_frame(robots, height, width, t):
    grid = np.zeros((height, width))
    robo_count = Counter([robot(t) for robot in robots])
    for(x, y) in robo_count:
        grid[y, x] = robo_count[(x, y)]
    plt.imshow(grid, cmap='viridis', interpolation='nearest')
    plt.title(f'Time step: {t}')
    plt.colorbar()
    plt.savefig(f'2024/14/imgs/frame_{t}.png')
    plt.close()

def create_gif(robots, height, width, start, end, filename='2024/14/output.gif'):
    frames = []
    for t in range(start, end + 1):
        save_frame(robots, height, width, t)
        frames.append(imageio.imread(f'2024/14/imgs/frame_{t}.png'))
    imageio.mimsave(filename, frames, duration=0.1)

def score_grid(robots, height=height, width=width):
    robo_count = Counter(robots)
    top_left = sum(v for k, v in robo_count.items() if k[0] < width//2 and k[1] < height//2)
    top_right = sum(v for k, v in robo_count.items() if k[0] > width//2 and k[1] < height//2)
    bottom_left = sum(v for k, v in robo_count.items() if k[0] < width//2 and k[1] > height//2)
    bottom_right = sum(v for k, v in robo_count.items() if k[0] > width//2 and k[1] > height//2)
    return top_left * top_right * bottom_left * bottom_right

def score_grid_FIXME(robots, height=height, width=width):
    robo_count = Counter(robots)
    xmid, ymid = width // 2, height // 2
    quads = [(-1, -1), (xmid, -1), (-1, ymid), (xmid, ymid)]
    quad_sums = [sum(v for k, v in robo_count.items() if qx < k[0] < qx + xmid and qy < k[1] < qy + ymid) for qx, qy in quads]
    print(robo_count)
    qx, qy = quads[2]
    print(f'qx={qx}, qy={qy}')
    test = {k: v for k, v in robo_count.items() if qx < k[0] < qx + xmid and qy < k[1] < qy + ymid}
    print(test) 
    print(quad_sums)
    return prod(quad_sums)

def is_xmas_tree(robots, height=height, width=width):
    robo_count = Counter(robots)
    tree_height = 0
    for y in range(height):
        if sum(robo_count[(x, y)] for x in range(width)) == tree_height*2 + 1:
            tree_height += 1
            for y2 in range(y+1, height):
                if sum(robo_count[(x, y2)] for x in range(width)) == tree_height*2 + 1:
                    tree_height += 1
                else:
                    break
            break
    return tree_height

def when_tree(robots, height=height, width=width):
    robo_count = Counter(robots)
    best_height = 0
    for t in range(100000):
        tree_height = is_xmas_tree([robot(t) for robot in robots])
        if tree_height > best_height:
            best_height = tree_height
            print(f'time={t}, height={best_height}')
            print_grid([robot(t) for robot in robots])


robots = [lambda t, init=init: find_location(init, t) for init in data]
# for t in range(100+1):
#     print(f'time={t}:')
#     print_grid([robot(t) for robot in robots])
# print_grid([robot(100) for robot in robots])
print('part1:', score_grid([robot(100) for robot in robots]))

# create_gif(robots, height, width, 0, height*width*0+1000)

min_score = inf
for t in range(height*width):
    score = score_grid([robot(t) for robot in robots])
    if score < min_score:
        min_score = score
        print(f'time={t}, score={score}')
        save_frame(robots, height, width, t)