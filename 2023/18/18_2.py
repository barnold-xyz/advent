from decimal import Decimal, getcontext

data = [line.split(' ') for line in open('2023/18/test.txt').read().split('\n')]

dir_map = dict(zip('RLUD', [(1, 0), (-1, 0), (0, -1), (0, 1)]))  # Updated to ensure x is horizontal and y is vertical
hex_to_dir = dict({'0':'R', '1':'D', '2':'L', '3':'U'})

# data will define a set of unit squares that are part of the trench
# we will store the coordinates of the *outside* of the trench
def parse_part3(data):
    x = y = 0
    trench = [(x, y)]  # Initial vertex
    width = 1  # Default trench width (1 block wide)
    trench_dist = 0

    for _,_,inst in data:
        inst = inst.strip('()#')
        length = int(inst[:5], 16)
        dir = hex_to_dir[inst[5]]

        # Add vertices based on direction
        if dir == 'U':  # Move up
            trench.append((x, y + length))
        elif dir == 'D':  # Move down
            trench.append((x, y - length))
        elif dir == 'L':  # Move left
            trench.append((x - length, y))
        elif dir == 'R':  # Move right
            trench.append((x + length, y))

        # Update the current position
        if dir == 'U':
            y += length
        elif dir == 'D':
            y -= length
        elif dir == 'L':
            x -= length
        elif dir == 'R':
            x += length

        trench_dist += length

    # Add the final corner vertices to close the trench
    trench.append((x + width, y))  # Right edge at the bottom
    trench.append((x + width, trench[0][1]))  # Right edge at the top
    trench.append((trench[0][0], trench[0][1]))  # Back to the starting point

    # increase trench_dist by the distance from the last vertex to the first
    trench_dist += abs(trench[-1][0] - trench[0][0]) + abs(trench[-1][1] - trench[0][1])

    # Return the trench vertices forming the outside of the trench
    return list(dict.fromkeys(trench)), trench_dist  # Removes duplicates, maintaining order


trench, trench_dist = parse_part3(data)
print(f'# trench vertices: {len(trench)}')

def solve_part2(trench, trench_dist):
    # Use the Shoelace formula to find the area of the trench
    area = Decimal(0)
    for i in range(len(trench) - 1):
        area += Decimal(trench[i][0]) * Decimal(trench[i + 1][1]) - Decimal(trench[i + 1][0]) * Decimal(trench[i][1])
    trench_area = abs(area) / 2
    print(f'Trench area: {trench_area}')

    # Calculate the perimeter (trench_dist)
    trench_dist = sum(((Decimal(trench[i][0]) - Decimal(trench[i - 1][0])) ** 2 + (Decimal(trench[i][1]) - Decimal(trench[i - 1][1])) ** 2).sqrt() for i in range(1, len(trench)))
    print(f'Trench perimeter: {trench_dist}')

    # Use Pick's theorem to find the number of points inside the trench
    points_inside_trench = (trench_area - trench_dist / 2 + 1)
    print(f'Points inside trench: {points_inside_trench}')
    
    total_points = trench_dist + points_inside_trench
    print(f'Total points: {total_points}')

solve_part2(trench, trench_dist)
quit()
# use matplotlib to plot the trench
import matplotlib.pyplot as plt
# Extract the vertices of the polygon
vertices = trench

# Plot the trench polygon
plt.figure(figsize=(8, 8))
x_coords, y_coords = zip(*vertices)
plt.plot(x_coords, y_coords, 'k-', marker='o')  # 'k-' means black solid line

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Trench Polygon')
plt.grid(True)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()