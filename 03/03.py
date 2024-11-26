import re

input = []

with open('03/input.txt', 'r') as file:
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

for row, line in enumerate(input):
    line_tokens = find_tokens(line)
    structured_tokens = [structure_token(token, row) for token in line_tokens]
    for token in structured_tokens:
        if token['type'] == 'number':
            part_numbers.append(token)
        if token['type'] == 'symbol':
            symbols.append(token)

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

def summarize_part1():
    return sum([part['value'] for part in part_numbers if is_valid_part_number(part)])

print(summarize_part1())

'''
# Debugging: Print out the matches
for line in input:
    matches = find_tokens(line)
    for match in matches:
        print(f"Match: {match[0]}, Start: {match[1]}")

print(symbols)
print(part_numbers)
'''