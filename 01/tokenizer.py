import re

data = []

with open('01/test2.txt', 'r') as file:
    for line in file:
        data.append(line.strip())

digit_map = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9
}

def tokenize(s):
    keywords = digit_map.keys()
    tokens = []
    while s:
        for keyword in keywords:
            if s.startswith(keyword):
                tokens.append(digit_map[keyword])
                s = s[len(keyword):]
                break
        else:
            tokens.append(s[0])
            s = s[1:]
    return tokens

print(tokenize('eightwothree'))
