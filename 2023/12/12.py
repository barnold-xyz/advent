import itertools
import re
from functools import cache

# Read and process the input data
with open("2023/12/input.txt") as f:
    data = [(line.split()[0], tuple(map(int, line.split()[1].split(',')))) for line in f.read().strip().split('\n')]

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
    return sum([1 for combo in combos if regex.match(combo)])

print('=========')

# following https://github.com/fuglede/adventofcode/blob/master/2023/day12/solutions.py
@cache
def count_combos(s, pattern, num_done_in_group=0):
    if not s: 
        return not pattern and not num_done_in_group
    num_solutions = 0
    possibilities = ['#', '.'] if s[0] == '?' else s[0]
    for p in possibilities:
        if p == '#':
            num_solutions += count_combos(s[1:], pattern, num_done_in_group + 1)
        else:
            if num_done_in_group:
                if pattern and pattern[0] == num_done_in_group:
                    num_solutions += count_combos(s[1:], pattern[1:])
            else:
                num_solutions += count_combos(s[1:], pattern)
    return num_solutions

# returns 5 copies of the string connected by 'separator'
def unfold_string(string):
    return '?'.join([string for _ in range(5)])

# repeat the patter 5 times
def unfold_pattern(pattern):
    return [item for _ in range(5) for item in pattern]

print(sum([count_combos(string+'.', pattern) for string, pattern in data]))
print(sum(
    count_combos(unfold_string(string)+'.', tuple(unfold_pattern(pattern))) for string, pattern in data
))
