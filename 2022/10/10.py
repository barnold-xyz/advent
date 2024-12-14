instructions = [line.split(' ') for line in open('2022/10/input.txt').read().splitlines()]

def run_cpu(instructions, max_t):
    cpu = [1]
    for t in range(max_t):
        cpu.append(cpu[-1])
        if not instructions:
            break
        op, *args = instructions.pop(0)
        if op == 'addx':
            t += 1
            cpu.append(cpu[-1] + int(args[0]))
    return cpu

def signal_strength(cpu):
    return sum(t*cpu[t-1] for t in range(20, 220+1, 40))
    #[print(f'{t}: {cpu[t-1]}') for t in range(20, 220+1, 40)]

def run_crt(cpu):
    print(cpu)
    crt = ''
    for t in range(len(cpu)):
        sprite_pos = cpu[t-1]
        # print(f'{t}: {sprite_pos}')
        if -1 <= sprite_pos - (t-1)%40 <= 1:
            crt += '#'
        else:
            crt += ' '

        if t % 40 == 0:
            crt += '\n'
    return crt

print('part 1:', signal_strength(run_cpu(instructions.copy(), 2500)))
print(run_crt(run_cpu(instructions.copy(), 2500)))