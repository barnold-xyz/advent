import re

data = []

with open('01/input.txt', 'r') as file:
    for line in file:
        data.append(line.strip())

def find_first_and_last_digit(s):
    first = re.search(r'\d', s).group()
    last = re.search(r'\d(?=\D*$)', s).group()
    return int(first+last)

def part1():
    return sum(list(map(find_first_and_last_digit, data)))

def part2():
    digit_map = {
        'one': 'o1ne',
        'two': 't2wo',
        'three': 't3hree',
        'four': 'f4our',
        'five':  'f5ive',
        'six': 's6ix',
        'seven': 's7even',
        'eight': 'e8ight',
        'nine': 'n9ine'
    }

    def replace_digits(s):
        for key in digit_map:
            s = s.replace(key, digit_map[key])
        return s
    
    return sum(list(map(find_first_and_last_digit, list(map(replace_digits, data)))))

print(part1())
print(part2())