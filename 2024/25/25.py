def parse_lock(lines):
    return [line.count('#') - 1 for line in zip(*lines)]

locks, keys = [], []
for d in open('2024/25/input.txt').read().split('\n\n'):
    lines = d.split('\n')
    if d.startswith('#####'):
        locks.append(parse_lock(lines))
    else:
        keys.append(parse_lock(reversed(lines)))

print('part 1:', sum(1 for l in locks for k in keys if max(a + b for a, b in zip(l, k)) <= 5))

