import itertools
import re

# Read and process the input data
with open("2023/12/test.txt") as f:
    data = [(line.split()[0], list(map(int, line.split()[1].split(',')))) for line in f.read().strip().split('\n')]

def pattern_to_regex(pattern):
    regex = f'#{{{pattern[0]}}}'
    regex += ''.join([f'\\#{{{n}}}' for n in pattern[1:]])
    return regex

print(pattern_to_regex([1, 1, 3]))

# Print the parsed data to verify
for pattern, numbers in data:
    print(f"Pattern: {pattern}, Numbers: {numbers}")

