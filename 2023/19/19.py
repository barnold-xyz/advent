import re

[workflow_list, parts_list] = [x.split('\n') for x in open("2023/19/input.txt").read().split('\n\n')]

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

#print(workflows)
#print(parts[0])
#print(workflows['in'][1])
#print(apply_rule(workflows['in'][1], parts[0]))

# we will now create a state machine to process the parts
# we will start in the 'in' state and progress through the states according to the rules
# we will stop when we reach the 'A' or 'R' state
def process_part(part, workflows):
    state = 'in'
    while state not in ['A', 'R']:
        for rule in workflows[state]:
            state = apply_rule(rule, part)
            if state is not None:
                break
    return state

print([process_part(part, workflows) for part in parts])
print(sum(sum(v for k, v in part.items()) for part in parts if process_part(part, workflows) == 'A'))