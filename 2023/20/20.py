from collections import deque
from math import lcm

data = open("2023/20/input.txt").read().split('\n')

graph = {}
flips = {}
conj = {}
counts = [0, 0]
button_presses = 0

def reset_graph():
    global counts, button_presses
    for line in data:
        src, _, *dest = line.replace(',','').split(' ')
        graph[src[1:]] = dest
        if src[0] == '%':
            flips[src[1:]] = 0
        elif src[0] == '&':
            conj[src[1:]] = {}

    for c in conj:
        conj[c] = {name: 0 for name in graph if c in graph[name]}

    nodes_to_add = {d for name in graph for d in graph[name] if d not in graph}
    graph.update({d: [] for d in nodes_to_add})

    counts = [0, 0]
    button_presses = 0

def push_button(cycle_check=[]):
    global button_presses
    button_presses += 1
    # signal is (source, hilo, dest)
    # type 0 is lo, type 1 is hi
    signal_queue = deque()
    signal_queue.append(('button', 0, 'roadcaster'))
    while signal_queue:
        (src, hilo, dest) = signal_queue.popleft()
        counts[hilo] += 1
        (new_src, new_hilo, new_dest) = (dest, None, graph[dest])
        
        # nand gate fires if all the inputs are 0
        if len(cycle_check)>0 and dest in cycle_check and hilo == 0:
            print(f'Cycle detected at iteration {button_presses} at node {src} cycle_check: {cycle_check}')
            return button_presses
        
        if dest in graph:
            if dest in flips:
                if not hilo:
                    if not flips[dest]:
                        flips[dest] = 1
                        new_hilo = 1
                    else:
                        flips[dest] = 0
                        new_hilo = 0
                else:
                    new_dest = []
            
            elif dest in conj:
                conj[dest][src] = hilo
                new_hilo = not all(conj[dest].values())
            
            else:
                new_hilo = hilo

            for d in new_dest: 
                signal_queue.append((new_src, new_hilo, d))

def test():
    reset_graph()
    push_button()
    print()
    push_button()
    print()
    push_button()
    print()
    push_button()
    print()

def part1():
    reset_graph()
    for _ in range(1000):
        push_button()
    print(counts[0]*counts[1])

def part2():
    reset_graph()
    # print everything that leads to 'rx'
    level1 = [k for k,v in graph.items() if 'rx' in v]
    print(level1)
    level2 = [k for k,v in graph.items() if any(l in level1 for l in v)]
    print(level2)
    
    cycle_times = []
    for node in level2:
        reset_graph()
        for _ in range(10000):
            if not push_button([node]) is None:
                cycle_times.append(button_presses)
                break
    print(cycle_times)
    print(lcm(*cycle_times))

part1()
part2()
