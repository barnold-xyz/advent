from collections import defaultdict

def dist(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)

sensors = {(xs, ys): (xb, yb) for (xs, ys, xb, yb) in [tuple(map(int, line.split(','))) 
        for line in open("2022/15/input.txt").read().replace('Sensor at x=', '').replace(' y=', '').replace(': closest beacon is at x=',',').replace(' y=', '').splitlines()]}

sensor_dists = {sensor: dist(*sensor, *beacon) for sensor, beacon in sensors.items()}

def find_coverage_in_row(sensors, row):
    coverage = set()
    for (xs, ys), (xb, yb) in sensors.items():
        max_dist = dist(xs, ys, xb, yb)
        if abs(ys - row) > max_dist:
            continue
        for xd in range(-max_dist, max_dist + 1): # this could be tightened up
            for yd in [row - ys]:
                if dist(xs, ys, xs+xd, ys+yd) <= max_dist and (xs+xd, ys+yd) not in sensors.values():    
                    coverage.add((xs+xd, ys+yd))
    return coverage

def find_beacon(sensors, sensor_dists, search_range=4000000):
    def is_valid_location(x, y):
        """Check if the given (x, y) is outside all sensor ranges."""
        for s in sensors:
            if dist(x, y, *s) <= sensor_dists[s]:
                return False
        return True
    
    # Check boundary locations for each sensor
    for s in sensors:
        sx, sy = s
        radius = sensor_dists[s] + 1  # Check just outside the exclusion zone

        # Generate boundary points for this sensor
        boundary_points = set()

        # Top and bottom edges
        for dx in range(-radius, radius + 1):
            boundary_points.add((sx + dx, sy - (radius - abs(dx))))  # Top
            boundary_points.add((sx + dx, sy + (radius - abs(dx))))  # Bottom

        # Left and right edges
        for dy in range(-radius, radius + 1):
            boundary_points.add((sx - (radius - abs(dy)), sy + dy))  # Left
            boundary_points.add((sx + (radius - abs(dy)), sy + dy))  # Right

        for x, y in boundary_points:
            if 0 <= x <= search_range and 0 <= y <= search_range:
                if is_valid_location(x, y):
                    return x, y  # Return the first valid beacon location

    return None  # No valid location found

def tuning_freq(x, y): 
    return x * 4000000 + y

print('part 1:', len(find_coverage_in_row(sensors, 2000000)))
print('part 2:', tuning_freq(*find_beacon(sensors, sensor_dists)))
# print_map(sensors)