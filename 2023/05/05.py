import bisect

def parse_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = {}
    current_map = None

    for line in lines:
        line = line.strip()
        if not line: continue
        if line.startswith("seeds:"):
            seeds = list(map(int, line.split(":")[1].strip().split()))
            data['seeds'] = seeds
        elif line.endswith("map:"):
            current_map = line[:-1].strip().replace(" ", "_").replace("-", "_")
            data[current_map] = []
        elif current_map:
            triplet = list(map(int, line.split()))
            data[current_map].append(triplet)

    # Sort triplets by the source number
    for key in data:
        if key != 'seeds':
            data[key] = sorted(data[key], key=lambda x: x[1])

    return data

parsed_data = parse_input('2023/05/input.txt')
seeds = parsed_data['seeds']

def efficient_map(triplet, key):
    #print(triplet)
    (dests, sources, lengths) = zip(*triplet)
    #print(sources)

    if key < sources[0]:
        return key
    elif key == sources[0]:
        return dests[0]

    pos = bisect.bisect_left(sources, key) - 1
    if pos < len(sources) - 1 and key == sources[pos + 1]:
        return dests[pos + 1]

    ref_low = sources[pos]
    ref_high = sources[pos] + lengths[pos] - 1

    if key < ref_low:  
        print(f"key {key} < ref_low {ref_low}")
        throw = 1/0
        return key

    if key > ref_high: 
        #print(f"key {key} > ref_high {ref_high}, pos {pos}")
        return key
    
    #print(dests)
    return dests[pos] + (key - ref_low)

def map_one(triplets, key):
    for (dest, src, size) in triplets:
        if src <= key < src + size:
            return key + dest - src
    return key

# List of [start, end) ranges
def map_ranges(triplets, ranges):
    adjusted_ranges = []
    for (dest, src, size) in triplets:
        src_end = src + size
        new_ranges = []
        while ranges:
            # [start                                     end)
            #          [src       src_end]
            # [BEFORE ][INTER            ][AFTER        )
            (start, end) = ranges.pop()
            # (src, size) might cut (start, end)
            before = (start, min(end, src))
            intersect = (max(start, src), min(src_end, end))
            after = (max(src_end, start), end)
            if before[1] > before[0]:
                new_ranges.append(before)
            if intersect[1] > intersect[0]:
                adjusted_ranges.append((intersect[0] - src + dest, intersect[1] - src + dest))
            if after[1] > after[0]:
                new_ranges.append(after)
        ranges = new_ranges
    return adjusted_ranges + ranges

def seed_to_location(seed):
    soil = map_one(parsed_data['seed_to_soil_map'], seed)
    fertilizer = map_one(parsed_data['soil_to_fertilizer_map'], soil)
    water = map_one(parsed_data['fertilizer_to_water_map'], fertilizer)
    light = map_one(parsed_data['water_to_light_map'], water)
    temperature = map_one(parsed_data['light_to_temperature_map'], light)
    humidity = map_one(parsed_data['temperature_to_humidity_map'], temperature)
    location = map_one(parsed_data['humidity_to_location_map'], humidity)
    return location

def seed_range_to_location(seed_ranges):
    soil = map_ranges(parsed_data['seed_to_soil_map'], seed_ranges)
    fertilizer = map_ranges(parsed_data['soil_to_fertilizer_map'], soil)
    water = map_ranges(parsed_data['fertilizer_to_water_map'], fertilizer)
    light = map_ranges(parsed_data['water_to_light_map'], water)
    temperature = map_ranges(parsed_data['light_to_temperature_map'], light)
    humidity = map_ranges(parsed_data['temperature_to_humidity_map'], temperature)
    location = map_ranges(parsed_data['humidity_to_location_map'], humidity)
    return location



def parse_seeds(seeds):
    seed_defs = [(x, y) for x, y in zip(seeds[::2], seeds[1::2])]
    #seed_list = [i for x, y in seed_defs for i in range(x, x + y + 1)]
    #return seed_list
    seed_ranges = [(x, x + y) for x, y in seed_defs]
    return seed_ranges

all_seeds = parse_seeds(seeds)


def summarize_part1():
    return min([seed_to_location(seed) for seed in seeds])

def summarize_part2():
    #return min([seed_to_location(seed) for seed in all_seeds])
    locs = seed_range_to_location(all_seeds)
    return min([l[0] for l in locs])

print(summarize_part1())
print(summarize_part2())
