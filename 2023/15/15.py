data = open("2023/15/input.txt").read().strip().split(',')

def hash(str):
    h = 0
    for c in str: 
        h += ord(c) 
        h *= 17
        h = h % 256
    return h

print(hash('HASH'))
print(sum([hash(d) for d in data]))