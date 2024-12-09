from collections import deque

data = open("2023/20/input.txt").read().split('\n')

graph = {}
flips = {}
conj = {}

for line in data:
    src, _, *dest = line.replace(',','').split(' ')
    graph[src[1:]] = dest
    if src[0] == '%':
        flips[src[1:]] = 0
    elif src[0] == '&':
        conj[src[1:]] = {}

for c in conj:
    conj[c] = {name: 0 for name in graph if c in graph[name]}

graph.update({d: [] for name in graph for d in graph[name]  if d not in graph})

counts = [0, 0]
def push_button():
    # signal is (source, hilo, dest)
    # type 0 is lo, type 1 is hi
    signal_queue = deque()
    signal_queue.append(('button', 0, 'roadcaster'))
    while signal_queue:
        (src, hilo, dest) = signal_queue.popleft()
        counts[hilo] += 1
        (new_src, new_hilo, new_dest) = (dest, None, graph[dest])
        #print(f'{src}\t{hilo}\t{dest}')
        
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

#print('\n'.join([f'{k}: {v}' for k,v in graph.items()]))
def test():
    push_button()
    print()
    push_button()
    print()
    push_button()
    print()
    push_button()
    print()

def part1():
    for _ in range(1000):
        push_button()
    print(counts[0]*counts[1])

part1()