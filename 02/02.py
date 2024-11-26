input = []

restrictions = {
    'red': 12,
    'green': 13,
    'blue': 14
}

with open('02/input.txt', 'r') as file:
    for line in file:
        input.append(line.strip())

def parse_draw(draw):
    colors = {'blue': 0, 'red': 0, 'green': 0}
    items = draw.split(',')
    for item in items:
        count, color = item.strip().split(maxsplit=1)
        colors[color] = int(count)
    return colors

def parse_game(s):
    parts = s.split(':')
    game_number = int(parts[0].strip().replace('Game ', ''))
    draws = parts[1].strip().split(';')
    draws = [parse_draw(draw.strip()) for draw in draws]
    return {
        'game_number': game_number,
        'draws': draws
    }

def is_valid_draw(draw):
    for color in draw:
        if draw[color] > restrictions[color]:
            return False
    return True

def is_valid_game(game): 
    return all(is_valid_draw(draw) for draw in game['draws'])

def summarize_part1(input):
    return sum([game['game_number'] for game in input if is_valid_game(game)])

def min_cubes_game(game):
    restrictions = { 'red': 0, 'green': 0, 'blue': 0 }
    for draw in game['draws']:
        for color in draw:
            restrictions[color] = max(restrictions[color], draw[color])
    return restrictions

def summarize_part2(input):
    restrictions = [min_cubes_game(game) for game in input]
    power = [r['red'] * r['green'] * r['blue'] for r in restrictions]
    return sum(power)

structured_data = [parse_game(game) for game in input]

#print(summarize_part1(structured_data))
print(summarize_part2(structured_data))
