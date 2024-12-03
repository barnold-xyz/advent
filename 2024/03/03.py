import re

data = open('2024/03/input.txt').read()

regex = r'mul\(\d{1,3},\d{1,3}\)'

def part1(data):
    matches = re.findall(regex, data)
    nums = [m[4:-1].split(',') for m in matches]
    print(sum([int(x) * int(y) for x, y in nums]))

def part2(data):
    parts = data.split('do()')
    total = sum(sum(x * y for x, y in [map(int, m[4:-1].split(',')) for m in re.findall(regex, part.split("don't()")[0])]) for part in parts)
    print(total)

part1(data)
part2(data)