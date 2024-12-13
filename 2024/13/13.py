import re
import numpy as np

machine_strs = open('2024/13/input.txt').read().split('\n\n')

pattern = re.compile(r'Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)')
machines = [tuple(map(int, pattern.search(machine_str).groups())) for machine_str in machine_strs]

def solve_presses(machine, part2=False):
    a, c, b, d, p, q = machine
    if part2:
        p += 10000000000000
        q += 10000000000000
    y = np.float64((a*q - c*p) / (a*d - b*c))
    x = np.float64((p - b*y) / a)
    err = np.float64(abs(x - int(x)) + abs(y - int(y)))
    if err > 1e-12:
        return 0, 0 
    return x, y

print(sum(3*s[0] + 1*s[1] for s in [solve_presses(machine) for machine in machines]))
print(sum(3*s[0] + 1*s[1] for s in [solve_presses(machine, part2=True) for machine in machines]))