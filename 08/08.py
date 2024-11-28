import networkx as nx
import math

def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)

def lcm_multiple(numbers):
    result = numbers[0]
    for number in numbers[1:]:
        result = lcm(result, number)
    return result

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

graph = nx.MultiDiGraph()
for node in network_def:
    name, children = parse_node(node)
    graph.add_node(name)
    left, right = children
    graph.add_edge(name, left, direction='L')
    graph.add_edge(name, right, direction='R')

def count_steps_to_zzz(instructions, graph):
    current = 'AAA'
    steps = 0
    instruction_len = len(instructions)
    while current != 'ZZZ' and steps < 1e6:
        next_int = instructions[steps % instruction_len]
        current = [v for u, v, d in graph.edges(current, data=True) if d['direction'] == next_int][0]
        steps += 1 
    return steps

def simultaneous_traverse_slow(instructions, graph):
    current = [node for node in graph if node.endswith('A')]
    print('current:', current)
    steps = 0
    instruction_len = len(instructions)
    at_end = False
    
    while (not at_end) and steps < 1e6:
        next_int = instructions[steps % instruction_len]
        current = [[v for u, v, d in graph.edges(n, data=True) if d['direction'] == next_int][0] for n in current]
        steps += 1 
        #print('current:', current)
        if all([node.endswith('Z') for node in current]): at_end = True
    return steps

def shortest_path_distance(graph, source, target):
    try:
        distance = nx.shortest_path_length(graph, source=source, target=target)
        return distance
    except nx.NetworkXNoPath:
        return None
    
start_nodes = [node for node in graph if node.endswith('A')]
end_nodes = [node for node in graph if node.endswith('Z')]

# AHA each starting node can only go to one ending node! 
distances = [len(instructions)]
for start_node in start_nodes:
    for end_node in end_nodes:
        dist = shortest_path_distance(graph, start_node, end_node)
        if dist is not None: distances.append(dist)

print(count_steps_to_zzz(instructions, graph))
print(lcm_multiple(distances))