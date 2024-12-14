data = open('2022/06/input.txt').read().split('\n')

# returns the index of the first time the previous n numbers are all different
def find_market_index(s, n=4):
    return next((i for i in range(n, len(s)) if len(set(s[i-n:i])) == n), None)

print([find_market_index(d) for d in data])
print([find_market_index(d, 14) for d in data])