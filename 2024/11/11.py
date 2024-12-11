from collections import defaultdict
import copy

#data = '125 17'
data = '890 0 1 935698 68001 3441397 7221 27'

stones = [int(x) for x in data.split()]

def blink(stones):
    new_stones = []
    for s in stones:
        if s == 0:
            new_stones.append(1)
        elif len(str(s)) % 2 == 0:
            str_s = str(s)
            new_stones.append(int(str_s[0:len(str_s)//2]))
            new_stones.append(int(str_s[len(str_s)//2:]))
        else:
            new_stones.append(s*2024)
    return new_stones

def pt1(stones):
    print(f'0: {stones}')
    for i in range(1, 25+1):
        stones = blink(stones)
        if i <= 6:
            print(f'{i}: {stones}')
        if i == 6: 
            print(len(stones))
    print(len(stones))

def pt2(stones):
    for i in range(1, 75+1):
        print(i)
        stones = blink(stones)
    print(len(stones))

def investigate():
    stones = [2024]
    for i in range(1, 10+1):
        stones = blink(stones)
        print(f'{i}: {len(stones)}')
        if 2024 in stones:
            print(f'2024 found in {i} iterations: {stones}')
            break

    stones = [40]
    print(f'checking 40')
    for i in range(1, 10+1):
        stones = blink(stones)
        print(f'{i}: {len(stones)}')
        if 2024 in stones:
            print(f'2024 found in {i} iterations: {stones}')
            break

def apply_rule(s):
    if s == 0:
        return [1]
    if len(str(s)) % 2 == 0:
        str_s = str(s)
        l = len(str_s) // 2
        return [int(str_s[0:l]), int(str_s[l:])]
    return [s*2024]

def loops_til_2024():
    loops = {}
    start_stone = 2024
    stones_2024 = [start_stone]
    for i in range(1, 30):
        stones_2024 = blink(stones_2024)
        print(f'{i}: {len(stones_2024)}, {stones_2024}')
        if 2024 in stones_2024:
            print(f'2024 found in {i} iterations: {stones_2024}')
            break

    for s in stones_2024:
        stones = [s]
        for i in range(1, 30):
            stones = blink(stones)
            if 2024 in stones:
                loops[s] = (i, stones)
                break
    [print(f'{k}: {v}') for k,v in loops.items()]
    return loops

# define a graph where each node is a stone and each edge is a transformation from one stone to another
# the transformation is a split if the stone is even, a multiply by 2024 if the stone is odd, and a change to 1 if the stone is 0
class Stone:
    def __init__(self, value, times=1):
        self.value = value
        self.edges = set()
        self.times = times

    def add_edge(self, edge):
        self.edges.add(edge)

    def __str__(self):
        return f'{self.value}: {self.edges}'

class StoneGraph:
    def __init__(self):
        self.graph = {}
        self.nodes = {}

    def add_node(self, value, times=1):
        if value not in self.nodes:
            self.nodes[value] = Stone(value, times)
        else:
            self.nodes[value].times += times

    def add_edge(self, src, dest):
        self.nodes[src].add_edge(dest)

    def blink_node(self, node):
        if node.times == 0:
            return
        if node.value == 0:
            self.add_node(1, 1)
            self.add_edge(node.value, 1)
            node.times -= 1
        elif len(str(node.value)) % 2 == 0:
            s = str(node.value)
            l = len(s) // 2
            n1 = int(s[0:l])
            n2 = int(s[l:])
            self.add_node(n1, 1)
            self.add_node(n2, 1)
            self.add_edge(node.value, n1)
            self.add_edge(node.value, n2)
            node.times -= 1
        else:
            self.add_node(node.value * 2024, 1)
            self.add_edge(node.value, node.value * 2024)
            node.times -= 1

    def blink(self):
        # Create a copy of the nodes to avoid modifying the dictionary while iterating
        nodes_copy = copy.deepcopy(list(self.nodes.values()))
        for node in nodes_copy:
            for _ in range(node.times):
                self.blink_node(self.nodes[node.value])

    def __print__(self):
        for node in self.nodes.values():
            print(node)

    def __len__(self):
        return sum(node.times for node in self.nodes.values())

    def printme(self):
        for node in sorted(self.nodes.values(), key=lambda x: x.value):
            if node.times > 0:
                print(f'{node.value} ({node.times}) -> {node.edges}')
        print(f'length: {len(self)}')
        print('---')


def part2(data):
    stones = StoneGraph()
    [stones.add_node(int(s)) for s in data.split()]

    for i in range(1, 25+1):
        stones.blink()
        print(f'iteration {i}, length={len(stones)}')

part2(data)
quit()

stones = StoneGraph()
stones.add_node(125)
stones.add_node(17)
#stones.add_node(2024)
for i in range(1, 25+1):
    stones.blink()
    print(f'iteration {i}: length={len(stones)}')
    #stones.printme()

quit()
# Example usage
stones = StoneGraph()
stones.add_node(0)
stones.blink()
stones.printme()
stones.blink()
stones.printme()
stones.blink()
stones.printme()
stones.blink()
stones.printme()
stones.blink()
stones.printme()
quit()


#loops_til_2024()

# strategy: create two data structures. The first is a map from starting stone to the list of stones generated after each iteration
# the second keeps track of how many times we have seen each number and what iteration it is on
# then we can find the length of the list after 75 iterations without actually generating the list
def part2(stones):


    seen = defaultdict(int)
    for i in range(0, 3+1):
        new_stones = []
        for s in stones:
            if seen[s] > 0:
                seen[s] += 1
                continue
            else:
                next_stones = apply_rule(s)
                new_stones.extend(next_stones)
                seen[s] += 1
        print(f'iteration {i}, stones={stones}')
        stones = new_stones
    #[print(f'{k}: {v}') for k,v in seen.items()]
    print(sum(seen.values()))

#part2(stones)
#investigate()
#pt1(stones)
#pt2(stones)