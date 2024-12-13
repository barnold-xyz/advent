data = [list(map(int, elf.split('\n'))) for elf in open('2022/01/input.txt').read().split('\n\n')]

print('part 1:', max(sum(elf) for elf in data))
print('part 2:', sum(sorted((sum(elf) for elf in data), reverse=True)[0:3]))