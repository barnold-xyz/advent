import sys
import re
from collections import defaultdict

# Read and parse the input file
data = open("05/input.txt").read().strip()
lines = data.split('\n')

# Split the data into parts
parts = data.split('\n\n')
seed_data, *function_data = parts
seed_values = [int(x) for x in seed_data.split(':')[1].split()]

class Function:
    def __init__(self, s):
        lines = s.split('\n')[1:]  # Ignore the first line (name)
        # Parse the tuples (destination, source, size)
        self.tuples: list[tuple[int, int, int]] = [[int(x) for x in line.split()] for line in lines]

    def apply_to_single_value(self, value):
        for (dest, src, size) in self.tuples:
            if src <= value < src + size:
                return value + dest - src
        return value

    # List of [start, end) ranges
    def apply_to_range(self, ranges):
        adjusted_ranges = []
        for (dest, src, size) in self.tuples:
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

# Create Function objects from the function data
functions = [Function(s) for s in function_data]

# Part 1: Apply functions to individual seed values
part1_results = []
for seed in seed_values:
    for function in functions:
        seed = function.apply_to_single_value(seed)
    part1_results.append(seed)
print(min(part1_results))

# Part 2: Apply functions to ranges of seed values
part2_results = []
seed_pairs = list(zip(seed_values[::2], seed_values[1::2]))
for start, size in seed_pairs:
    # Inclusive on the left, exclusive on the right
    # e.g. [1,3) = [1,2]
    # Length of [a,b) = b-a
    # [a,b) + [b,c) = [a,c)
    ranges = [(start, start + size)]
    for function in functions:
        ranges = function.apply_to_range(ranges)
    part2_results.append(min(ranges)[0])
print(min(part2_results))