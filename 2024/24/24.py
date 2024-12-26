import networkx as nx

input_str, gate_str = open('2024/24/input.txt').read().split('\n\n')

gates = nx.DiGraph()

for g in gate_str.split('\n'): 
    input1, gate_type, input2, _, output = g.split(' ')
    gates.add_edge(input1, output)
    gates.add_edge(input2, output)
    gates.nodes[output]['gate_type'] = gate_type
    gates.nodes[output]['wire_value'] = None

for i in input_str.split('\n'): 
    gate, input = i.split(': ')
    gates.nodes[gate]['gate_type'] = 'input'
    gates.nodes[gate]['wire_value'] = int(input)

while any([gates.nodes[n]['wire_value'] is None for n in gates.nodes]):
    # traverse the grid from the input nodes onwards
    for node in nx.topological_sort(gates): 
        if gates.nodes[node]['gate_type'] == 'input': 
            continue
        input1, input2 = gates.predecessors(node)
        input1_value = gates.nodes[input1]['wire_value']
        input2_value = gates.nodes[input2]['wire_value']
        if gates.nodes[node]['gate_type'] == 'AND': 
            gates.nodes[node]['wire_value'] = input1_value & input2_value
        elif gates.nodes[node]['gate_type'] == 'OR': 
            gates.nodes[node]['wire_value'] = input1_value | input2_value
        elif gates.nodes[node]['gate_type'] == 'XOR': 
            gates.nodes[node]['wire_value'] = input1_value ^ input2_value
        else: 
            raise Exception('Unknown gate type')

print('part 1:', int(''.join(str(gates.nodes[n]['wire_value']) for n in sorted(gates.nodes, reverse=True) if n.startswith('z')), 2))

