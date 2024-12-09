import re
from collections import deque

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
print('starting part 2')
# part 2

# help from https://github.com/jonathanpaulson/AdventOfCode/blob/master/2023/19.py
def new_range(op, n, lo, hi):
    if op=='>':
        lo = max(lo, n+1)
    elif op=='<':
     hi = min(hi, n-1)
    elif op=='>=':
     lo = max(lo, n)
    elif op=='<=':
      hi = min(hi, n)
    else:
      assert False
    return (lo,hi)

def new_ranges(var, op, n, xl,xh,ml,mh,al,ah,sl,sh):
    if var=='x':
        xl,xh = new_range(op, n, xl, xh)
    elif var=='m':
      ml,mh = new_range(op, n, ml, mh)
    elif var=='a':
        al,ah = new_range(op, n, al, ah)
    elif var=='s':
       sl,sh = new_range(op, n, sl, sh)
    return (xl,xh,ml,mh,al,ah,sl,sh)

ans = 0
Q = deque([('in', 1, 4000, 1, 4000, 1, 4000, 1,4000)])
while Q:
    state, xl, xh, ml, mh, al, ah, sl, sh = Q.pop()
    if xl > xh or ml > mh or al > ah or sl > sh:
        continue
    if state == 'A':
        score = (xh - xl + 1) * (mh - ml + 1) * (ah - al + 1) * (sh - sl + 1)
        ans += score
        continue
    elif state == 'R':
        continue
    else:
        for rule in workflows[state]:
            res = rule['new_flow']
            if rule.get('cat') is None:
                Q.append((res, xl, xh, ml, mh, al, ah, sl, sh))
                break
            else:
                var = rule['cat']
                op = rule['func']
                n = rule['lim']
                Q.append((res, *new_ranges(var, op, n, xl, xh, ml, mh, al, ah, sl, sh)))
                xl, xh, ml, mh, al, ah, sl, sh = new_ranges(var, '<=' if op == '>' else '>=', n, xl, xh, ml, mh, al, ah, sl, sh)

print(ans)