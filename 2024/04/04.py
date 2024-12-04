data = [list(row) for row in open("2024/04/input.txt").read().split('\n')]

def find_word(data, target):
    coords = []
    for y, row in enumerate(data):
        for x, cell in enumerate(row):
            if cell == target[0]:
                for dir in [(1, 0), (0, 1), (-1, 0), (0,-1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
                    if 0 <= x + (len(target) - 1) * dir[0] < len(data[0]) and 0 <= y + (len(target) - 1) * dir[1] < len(data):
                        if all(data[y + i * dir[1]][x + i * dir[0]] == target[i] for i in range(1, len(target))):
                            coords.append((x, y))
    return coords

def find_x_mas(data):
    coords = []
    for y, row in enumerate(data):
        for x, cell in enumerate(row):
            if 1 <= x < len(data[0]) - 1 and 1 <= y < len(data) - 1 and cell == 'A':
                top_left_bot_right = data[y-1][x-1] + cell + data[y+1][x+1]
                top_right_bot_left = data[y-1][x+1] + cell + data[y+1][x-1]
                if top_left_bot_right in ['MAS','SAM'] and top_right_bot_left in ['MAS','SAM']:
                    coords.append((x, y))
    return coords

xmas_coords = find_word(data, 'XMAS')
print(len(xmas_coords))
x_mas_coords = find_x_mas(data)
print(len(x_mas_coords))