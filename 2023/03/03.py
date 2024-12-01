import re

input = []

with open('2023/03/input.txt', 'r') as file:
    for line in file:
        input.append(line.strip())

# Each token has coordinates in a 2D grid, row and starting column
# We will use a dictionary to store the coordinates of each token
def display_match(match):
    if match is None:
        return None
    return '<Match: %r, groups=%r>' % (match.group(), match.groups())

def find_tokens(line):
    pattern = re.compile(r'\d+|[^\d.]+')
    matches = pattern.finditer(line)
    tokens = [(match.group(), match.start()) for match in matches]
    return tokens

def structure_token(token, row):
    value, col = token
    if value.isdigit():
        return {
            'type': 'number',
            'value': int(value),
            'row': row,
            'col': col
        }
    else:
        return {
            'type': 'symbol',
            'value': value,
            'row': row,
            'col': col
        }

part_numbers = []
symbols = []
possible_gears = []
for row, line in enumerate(input):
    line_tokens = find_tokens(line)
    structured_tokens = [structure_token(token, row) for token in line_tokens]
    for token in structured_tokens:
        if token['type'] == 'number':
            part_numbers.append(token)
        if token['type'] == 'symbol':
            symbols.append(token)
            if token['value'] == '*':
                possible_gears.append(token)

def is_valid_part_number(part_number):
    if part_number['type'] != 'number': return False

    row = part_number['row']
    start_col = part_number['col']
    end_col = start_col + len(str(part_number['value'])) - 1
    
    symbol_rows = [row-1, row, row+1]
    symbol_cols = list(range((start_col-1), (end_col+1) + 1)) #extends 1 col each way bc diagonals count
    symbol_coordinates = [(r, c) for r in symbol_rows for c in symbol_cols]
    
    # slow to run thru this every time
    for symbol in symbols:
        if (symbol['row'], symbol['col']) in symbol_coordinates:
            return True
    return False

def calc_gear_ratio(gear):
    row = gear['row']
    col = gear['col']
    
    valid_part_rows = [row-1, row, row+1]
    valid_part_cols = [col-1, col, col+1]
    valid_part_coordinates = [(r, c) for r in valid_part_rows for c in valid_part_cols]

    parts_touching = []
    for part in part_numbers:
        part_row = part['row']
        part_col = part['col']
        part_cols = list(range(part_col, part_col + len(str(part['value']))))
        part_coordinates = [(part_row, c) for c in part_cols]
        if any([coord in valid_part_coordinates for coord in part_coordinates]):
            parts_touching.append(part)

    if len(parts_touching) == 2:
        return parts_touching[0]['value'] * parts_touching[1]['value']
    else:
         return 0

def summarize_part1():
    return sum([part['value'] for part in part_numbers if is_valid_part_number(part)])

def summarize_part2():
    return sum([calc_gear_ratio(gear) for gear in possible_gears])

print(summarize_part1())
print(summarize_part2())