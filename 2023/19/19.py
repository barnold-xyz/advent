import re

[workflow_list, parts_list] = [x.split('\n') for x in open("2023/19/test.txt").read().split('\n\n')]

func_map = {'<': lambda x, y: x < y, '>': lambda x, y: x > y}

def parse_rule(rule_str):
    if not ':' in rule_str: 
        return {'new_flow': rule_str}

    match = re.match(r'(?P<cat>[a-zA-Z])(?P<func>[<>=])(?P<lim>\d+):(?P<new_flow>[a-zA-Z]+)', rule_str)
    if match:
        rule = match.groupdict()
        rule['lim'] = int(rule['lim'])
        return rule
    else:
        raise ValueError(f"Invalid rule format: {rule_str}")

def parse_part(part_str):
    pairs = re.findall(r'(\w+)=(\d+)', part_str.strip('{}'))
    return {key: int(value) for key, value in pairs}

def apply_rule(rule, part):
    if rule.get('cat') is None: return rule['new_flow'] 
    
    if func_map[rule['func']](part[rule['cat']], rule['lim']):
        return rule['new_flow']
    else: 
        return None

workflows = {name: [parse_rule(rule) for rule in rules.split(',')]
             for name, rules in (flow.strip('}').split('{') 
                                 for flow in workflow_list)}

parts = [parse_part(part) for part in parts_list]

# we will now create a state machine to process the parts
def process_part(part, workflows):
    state = 'in'
    while state not in ['A', 'R']:
        for rule in workflows[state]:
            state = apply_rule(rule, part)
            if state is not None:
                break
    return state

#print([process_part(part, workflows) for part in parts])
print(sum(sum(v for k, v in part.items()) for part in parts if process_part(part, workflows) == 'A'))

# part 2
# this would work if we had infinite time
#print(sum(1 for x in range(1, 4001) 
#          for m in range(1, 4001)
#          if process_part({'x': x, 'm': m, 'a': 0, 's': 0}, workflows) == 'A'))

# procedure: work backwards from state A to find the valid starting inputs

possible_x = possible_m = possible_a = possible_s = range(1, 4001)
possible = {}
for cat in ['x', 'm', 'a', 's']: possible[cat] = range(1, 4001)
#print(workflows)

state = 'R'
flows = [flow for flow in workflows if any(rule['new_flow'] == 'A' for rule in workflows[flow])]
for flow in flows:
    for rule in workflows[flow]:
        if rule['new_flow'] == 'R':
            print(rule)
            if rule.get('cat') is None: continue
            possible[rule['cat']] = [x for x in possible[rule['cat']] if func_map[rule['func']](x, rule['lim'])]
    
print(len(possible['x']) * len(possible['m']) * len(possible['a']) * len(possible['s']))