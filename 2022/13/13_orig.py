def read_input(file):
    return [[eval(element) for element in line.split('\n')] for line in open(file).read().split('\n\n')]

def pairwise_comp(p1, p2, debug=False):
    if debug: print(f'comparing {p1} and {p2}')
    comp = 0
    while not comp:
        if not p1 and not p2: return 1
        if not p2: return -1
        if not p1: return 1

        if p1 == p2: return 0

        if isinstance(p1, int) and isinstance(p2, int):
            if p1 == p2: continue
            else: comp = 1 if p1 < p2 else -1
        elif isinstance(p1, list) and isinstance(p2, list):
            e1, e2 = p1.pop(0), p2.pop(0)
            comp = pairwise_comp(e1, e2, debug)
            # print(f'list comparison: {comp}')
        elif isinstance(p1, int) and isinstance(p2, list):
            comp = pairwise_comp([p1], p2, debug)
        elif isinstance(p1, list) and isinstance(p2, int):
            comp = pairwise_comp(p1, [p2], debug)
        else:
            return 0

    return comp

file = '2022/13/test0.txt'
def test():
    data = read_input(file)
    for num in range(len(data)):
        print('---')
        print(num+1)
        print(num+1, pairwise_comp(data[num][0], data[num][1], debug=True))
test()
data = read_input(file)
print(sum(i+1 for i in range(len(data)) if pairwise_comp(data[i][0], data[i][1], debug=False) == 1))
