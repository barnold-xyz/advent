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

parsed_data = parse_input('05/input.txt')
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



def seed_to_location(seed):
    soil = efficient_map(parsed_data['seed_to_soil_map'], seed)
    fertilizer = efficient_map(parsed_data['soil_to_fertilizer_map'], soil)
    water = efficient_map(parsed_data['fertilizer_to_water_map'], fertilizer)
    light = efficient_map(parsed_data['water_to_light_map'], water)
    temperature = efficient_map(parsed_data['light_to_temperature_map'], light)
    humidity = efficient_map(parsed_data['temperature_to_humidity_map'], temperature)
    location = efficient_map(parsed_data['humidity_to_location_map'], humidity)
    return location

def summarize_part1():
    return min([seed_to_location(seed) for seed in seeds])

print(summarize_part1())



seed_to_soil_map = parsed_data['seed_to_soil_map']
soil_to_fertilizer_map = parsed_data['soil_to_fertilizer_map']
fertilizer_to_water_map = parsed_data['fertilizer_to_water_map']
water_to_light_map = parsed_data['water_to_light_map']
light_to_temperature_map = parsed_data['light_to_temperature_map']
temperature_to_humidity_map = parsed_data['temperature_to_humidity_map']
humidity_to_location_map = parsed_data['humidity_to_location_map']

