import math

def init_monkeys():
    return [
        {
            'items': list(map(int, d.split('\n')[1].replace('Starting items: ', '').split(', '))),
            'op': d.split('\n')[2].replace('Operation: new = ', '').strip(),
            'test': int(d.split('\n')[3].replace('Test: divisible by ', '')),
            'test_true': int(d.split('\n')[4].replace('If true: throw to monkey ', '')),
            'test_false': int(d.split('\n')[5].replace('If false: throw to monkey ', '')),
            'inspections': 0
        }
        for d in open('2022/11/input.txt').read().split('\n\n')
    ]

factor = math.prod(m['test'] for m in init_monkeys())

def print_monkeys(monkeys):
    for i, m in enumerate(monkeys):
        print(f'monkey {i}: {m["items"]}')
    print()

def run_round(monkeys, part1=True): 
    for m in monkeys:
        while m['items']:
            old = m['items'].pop(0)
            m['inspections'] += 1
            worry = eval(m['op'])
            worry = worry % factor
            if part1: 
                worry = worry // 3
            dest = m['test_true'] if worry % m['test'] == 0 else m['test_false']
            monkeys[dest]['items'].append(worry)

def run_sim(rounds, part1):
    monkeys = init_monkeys()
    for i in range(rounds):
        run_round(monkeys, part1)
    inspections = sorted(m['inspections'] for m in monkeys)
    return inspections[-1] * inspections[-2]

print('part 1:', run_sim(20, True))
print('part 2:', run_sim(10000, False))
          