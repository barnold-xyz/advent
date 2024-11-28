# Read and parse the input file
data = open("08/input.txt").read().strip().split('\n\n')

def parse_node(node):
    name, left_right = node.split('=')
    name = name.strip()
    left, right = left_right.strip().strip('()').split(',')
    left = left.strip()
    right = right.strip()
    return name, (left, right)

instructions = data[0]
network_def = data[1].split('\n')

graph = {}

for node in network_def:
    name, children = parse_node(node)
    graph[name] = children

def count_steps_to_zzz(instructions, graph):
    current = 'AAA'
    steps = 0
    instruction_len = len(instructions)
    while current != 'ZZZ' and steps < 100000:
        if instructions[steps % instruction_len] == 'L':
            current = graph[current][0]
        elif instructions[steps % instruction_len] == 'R':
            current = graph[current][1]
        steps += 1 
    return steps

#print(count_steps_to_zzz(instructions, graph))

print(graph)

def simultaneous_traverse(instructions, graph):
    current = [node for node in graph if node.endswith('A')]
    at_end = False
    print('current:', current)
    steps = 0
    instruction_len = len(instructions)
    while (not at_end) and steps < 1e8:
        if instructions[steps % instruction_len] == 'L':
            current = [graph[node][0] for node in current]
        elif instructions[steps % instruction_len] == 'R':
            current = [graph[node][1] for node in current]
        steps += 1 
        #print('current:', current)
        if all([node.endswith('Z') for node in current]): at_end = True
    return steps

print(simultaneous_traverse(instructions, graph))