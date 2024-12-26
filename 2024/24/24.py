input_str, gate_str = open('2024/24/test.txt').read().split('\n\n')

class Gate: 
    def __init__(self, gate_type, input_gates, output_gate): 
        self.gate = gate_type
        self.input_gates = input_gates
        self.input_values = [None] * len(input_gates)
        self.output = output_gate
        self.output_value = None

    def __str__(self): 
        return f'{self.gate} {self.input_gates} {self.input_values} {self.output}, {self.output_value}'

gates = {}
inputs = {}
for i in input_str.split('\n'): 
    gate, input = i.split(': ')
    gates[gate] = Gate('input', [], gate)
    inputs[gate] = int(input)

for g in gate_str.split('\n'): 
    input1, gate_type, input2, _, output = g.split(' ')
    if output in gates:
        raise Exception('Gate already exists')
    if not output in gates: 
        gates[output] = Gate(gate_type, [input1, input2], output)

print(gates['z00'])