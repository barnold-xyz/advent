from collections import deque
import copy

crate_str, inst_str = open('2022/05/input.txt').read().split('\n\n')

def transpose(matrix):
    return list(map(list, zip(*matrix)))

crate_str = [crate.replace('[', ' ').replace(']', ' ') for crate in crate_str.split('\n')[:-1]]
crate_str = [(''.join(c)).strip() for c in transpose(crate_str)]
crates = [deque(c) for c in crate_str if c]

print(crates)

inst = [i.replace('move ','').replace(' from ', ' ').replace(' to ', ' ').split(' ') for i in inst_str.split('\n')]

def move_crate(crates, inst):
    num_crates, source, dest = int(inst[0]), int(inst[1])-1, int(inst[2])-1
    for i in range(num_crates):
        crates[dest].appendleft(crates[source].popleft())
    return crates

def move_crate_pt2(crates, inst):
    num_crates, source, dest = int(inst[0]), int(inst[1])-1, int(inst[2])-1
    crates[source] = list(crates[source])
    crates_to_move = crates[source][0:num_crates]
    #print(f'crates to move: {crates_to_move}')
    crates[source] = crates[source][num_crates:]
    crates[dest] = crates_to_move + list(crates[dest])
    return crates
    
crates_pt1 = copy.deepcopy(crates)
for i in inst:
    crates_pt1 = move_crate(crates_pt1, i)

print('part 1:', ''.join(c[0] for c in crates_pt1))

for i in inst:
    crates = move_crate_pt2(crates, i)
    print(crates)

print('part 2:', ''.join(c[0] for c in crates))
