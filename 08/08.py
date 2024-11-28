import networkx as nx

data = open("08/test3.txt").read().strip().split('\n\n')

def parse_node(node):
    name, left_right = node.split('=')
    name = name.strip()
    left, right = left_right.strip().strip('()').split(',')
    left = left.strip()
    right = right.strip()
    return name, (left, right)

instructions = data[0]
network_def = data[1].split('\n')

# Initialize the graph
graph = nx.MultiDiGraph()

# Parse each node and add it to the graph
for node in network_def:
    name, children = parse_node(node)
    graph.add_node(name)
    left, right = children
    graph.add_edge(name, left, direction='L')
    graph.add_edge(name, right, direction='R')

print(graph.nodes())
print(graph.edges(data=True))

def count_steps_to_zzz(instructions, graph):
    current = 'AAA'
    steps = 0
    instruction_len = len(instructions)
    while current != 'ZZZ' and steps < 1e6:
        next_int = instructions[steps % instruction_len]
        current = [v for u, v, d in graph.edges(current, data=True) if d['direction'] == next_int][0]
        steps += 1 
    return steps

#print(count_steps_to_zzz(instructions, graph))

def simultaneous_traverse_slow(instructions, graph):
    current = [node for node in graph if node.endswith('A')]
    print('current:', current)
    steps = 0
    instruction_len = len(instructions)
    at_end = False
    
    while (not at_end) and steps < 1e8:
        if instructions[steps % instruction_len] == 'L':
            current = [list(graph.successors(node))[0] if len(list(graph.successors(node))) > 0 else node for node in current]
        elif instructions[steps % instruction_len] == 'R':
            current = [list(graph.successors(node))[1] if len(list(graph.successors(node))) > 1 else node for node in current]
        steps += 1 
        #print('current:', current)
        if all([node.endswith('Z') for node in current]): at_end = True
    return steps

#print(simultaneous_traverse_slow(instructions, graph))
#print([node for node in graph if node.endswith('Z')])
