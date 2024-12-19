from functools import lru_cache

towels, designs = map(lambda x: x.replace(', ','\n').split(), open('2024/19/input.txt').read().split('\n\n'))

@lru_cache(None)
def dfs(towels, design):
    if not design:
        return 1
    count = 0
    for t in towels:
        if design.startswith(t):
            count += dfs(towels, design[len(t):])
    return count
            
results = [dfs(tuple(towels), design) for design in designs]
print('part 1:', sum(1 for result in results if result > 0))
print('part 2:', sum(results))