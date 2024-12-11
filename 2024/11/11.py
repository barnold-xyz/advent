import cProfile
import pstats
import io
import copy

#data = '125 17'
data = '890 0 1 935698 68001 3441397 7221 27'

stones = [int(x) for x in data.split()]

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

    def blink_node(self, node, times=1):
        if node.times == 0:
            return
        if node.value == 0:
            self.add_node(1, times)
            self.add_edge(node.value, times)
            node.times -= times
        elif len(str(node.value)) % 2 == 0:
            s = str(node.value)
            l = len(s) // 2
            n1 = int(s[0:l])
            n2 = int(s[l:])
            self.add_node(n1, times)
            self.add_node(n2, times)
            self.add_edge(node.value, n1)
            self.add_edge(node.value, n2)
            node.times -= times
        else:
            self.add_node(node.value * 2024, times)
            self.add_edge(node.value, node.value * 2024)
            node.times -= times

    def blink(self):
        # Create a copy of the nodes to avoid modifying the dictionary while iterating
        nodes_copy = copy.deepcopy(list(self.nodes.values()))
        for node in nodes_copy:
            #for _ in range(node.times):
                self.blink_node(self.nodes[node.value], node.times)

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

def part1(data):
    stones = StoneGraph()
    [stones.add_node(int(s)) for s in data.split()]

    for i in range(1, 25+1):
        stones.blink()
        print(f'iteration {i}, length={len(stones)}, nodes={len(stones.nodes)}')

def part2(data):
    stones = StoneGraph()
    [stones.add_node(int(s)) for s in data.split()]

    for i in range(1, 75+1):
        stones.blink()
        print(f'iteration {i}, length={len(stones)}, nodes={len(stones.nodes)}')

part1(data)

# Profile the part2 function
pr = cProfile.Profile()
pr.enable()
part2(data)
pr.disable()

# Print profiling results
s = io.StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
ps.print_stats()
print(s.getvalue())