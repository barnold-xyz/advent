from collections import Counter

# Initialize two empty lists
list1, list2 = [], []

with open('2024/01/input.txt', 'r') as file:
    data = [list(map(int, line.split())) for line in file]

list1, list2 = zip(*data)
list1, list2 = sorted(list1), sorted(list2)
counter = Counter(list2)

print(sum(abs(y - x) for x, y in zip(list1, list2)))

print(sum([x * counter[x] for x in list1]))
