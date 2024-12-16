grid = {(x, y): c for y, row in enumerate(open('2022/12/input.txt').read().splitlines()) for x, c in enumerate(row)}
height = max(y for x, y in grid) + 1
width = max(x for x, y in grid) + 1
start = next(k for k, v in grid.items() if v == 'S')
end = next(k for k, v in grid.items() if v == 'E')
grid[start] = 'a'
grid[end] = 'z'

def print_grid(pos=[start]):
    def letter_to_rgb(letter):
        """Convert a letter from 'a' to 'z' to an RGB value for the gradient."""
        min_val, max_val = ord('a'), ord('z')
        value = ord(letter)
        ratio = (value - min_val) / (max_val - min_val)  # Normalize to 0-1 range

        # Gradient from red to blue
        r = int(255 * (1 - ratio))
        g = 0
        b = int(255 * ratio)

        return r, g, b

    def rgb_to_ansi(r, g, b):
        """Convert RGB to an ANSI escape code."""
        return f"\033[38;2;{r};{g};{b}m"

    for y in range(height):
        for x in range(width):
            if (x, y) in pos:
                print('#', end='')
            elif (x, y) == start:
                print('S', end='')
            elif (x, y) == end:
                print('E', end='')
            else:
                char = grid.get((x, y), ' ')
                if char.islower():  # Only apply gradient to letters
                    r, g, b = letter_to_rgb(char)
                    color = rgb_to_ansi(r, g, b)
                    print(f"{color}{char}\033[0m", end='')  # Reset color after printing
                else:
                    print(char, end='')
        print()

def bfs(start=start, ends=[end]):
    queue = [(start, 0, [start])]
    visited = {start}
    while queue:
        pos, dist, path = queue.pop(0)
        if pos in ends:
            return path
        x, y = pos
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_pos = x + dx, y + dy
            if new_pos in grid and new_pos not in visited and ord(grid[new_pos]) - ord(grid[pos]) <= 1:
                visited.add(new_pos)
                queue.append((new_pos, dist + 1, path + [new_pos]))

path1 = bfs(start, [end])
print_grid(path1)
print('part 1:', len(path1) - 1)

grid = {k: chr(ord('a') + ord('z') - ord(v)) if v.islower() else v for k, v in grid.items()}
path2 = bfs(end, [k for k, v in grid.items() if v == 'z'])
print_grid(path2)
print('part 2:', len(path2) - 1)

