import itertools
import re

# Read and process the input data
with open("2023/12/input.txt") as f:
    data = [(line.split()[0], list(map(int, line.split()[1].split(',')))) for line in f.read().strip().split('\n')]

def pattern_to_regex(pattern):
    regex = f'\\.*#{{{pattern[0]}}}'
    regex += ''.join([f'\\.+#{{{n}}}' for n in pattern[1:]])
    regex += f'\\.*$'
    return regex

def generate_combos(s):
    if len(s) == 1: 
        return ['#', '.'] if s == '?' else [s]
    return [c + rest for c in generate_combos(s[0]) for rest in generate_combos(s[1:])]


def summarize_line_pt1(line):
    string, pattern = line
    regex = re.compile(pattern_to_regex(pattern))
    combos = generate_combos(string)
    matches = [combo for combo in combos if regex.match(combo)]
    #print(string, pattern, regex, combos, matches)
    return sum([1 for combo in combos if regex.match(combo)])

#print(summarize_line_pt1(data[1]))
print([summarize_line_pt1(line) for line in data])
print(sum([summarize_line_pt1(line) for line in data]))

quit()
print('=========')

line = data[-1]
regex = re.compile(pattern_to_regex(line[1]))
combos = generate_combos(line[0])
for combo in combos:
    print(combo, regex.match(combo))
print(regex)