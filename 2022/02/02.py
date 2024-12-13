strategy = [line.split(' ')  for line in open('2022/02/input.txt').read().strip().split('\n')]

score_map = {'A': 1, 'B': 2, 'C': 3, 'X': 1, 'Y': 2, 'Z': 3}
scores = list(score_map.values())

def score(p1, p2): 
    return p2 + (3 if p2 == p1 else 6 if p2 - p1 in [1, -2] else 0)

def score_part2(p1, p2):
    return scores[scores.index(p1) + p2 - 2] + (p2 - 1)* 3

print('part1 ', sum(score(score_map[p1], score_map[p2]) for p1, p2 in strategy))
print('part2 ', sum(score_part2(score_map[p1], score_map[p2]) for p1, p2 in strategy))