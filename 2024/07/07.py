from math import prod
import itertools

data = open("2024/07/input.txt").read().split('\n')

def add(x,y): return x+y
def mult(x,y): return x*y
fn_list = [add, mult]

def test_line(line):
    target, args = line.split(':')
    target = int(target)
    args = list(map(int, args.strip().split(' ')))
    running_total = 0

    #stack = []
    #[stack.append([fn(args[0], args[1])] + args[2:]) for fn in fn_list]
    stack = [args]
    while stack:
        current = stack.pop()
        #print(f"Current stack: {stack}")    
        if len(current) == 1:
            if current[0] == target:
                return target
        else: 
            for fn in fn_list:
                new_stack = [fn(current[0], current[1])] + current[2:]
                stack.append(new_stack)
                #print(f"New stack appended: {new_stack}")
        #print(f"Stack after append: {stack}")
        #print(f"Stack length: {len(stack)}")
    return 0
    
print(sum(test_line(line) for line in data))

