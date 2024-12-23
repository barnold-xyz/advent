import numpy as np

seeds = np.loadtxt('2024/22/test.txt', dtype=int)
# seeds = [123]
# seeds = np.array([1])

def hash_sequence(seeds, n_iterations=2000):
    result = np.zeros((len(seeds), n_iterations + 1), dtype=np.int64)
    result[:, 0] = seeds  

    MOD = 16777216  # 2^24
    
    for i in range(n_iterations):
        current = result[:, i]
        secret = (current ^ (current * 64)) % MOD
        secret = (secret ^ (secret // 32)) % MOD
        secret = (secret ^ (secret * 2048)) % MOD
        result[:, i + 1] = secret
    return result

# iterate over the sequences that are acutally in the data
def find_best_seq(prices, diffs):
    window_size = 4
    
    # Initialize variables
    seen_sequences = set()
    best_sequence = None
    max_total_price = 0

    def calc_score(prices, diffs, sequence):
        score = 0
        window_size = len(sequence)
        for p in prices:
            for i in range(len(p) - window_size):
                if tuple(p[i:i+window_size]) == tuple(sequence):
                    score += p[i+window_size]
                    break
        return score

    for p in prices:
        for i in range(len(p) - window_size):
            if tuple(p[i:i+window_size]) in seen_sequences:
                continue
            seen_sequences.add(tuple(p[i:i+window_size]))
            score = calc_score(prices, diffs, p[i:i+window_size])
            if score > max_total_price:
                best_sequence = p[i:i+window_size]
                max_total_price = score
                print(f'new best sequence: {best_sequence} with score {max_total_price}')

    return best_sequence, max_total_price

    

sequences = hash_sequence(seeds)
prices = np.apply_along_axis(lambda x: x % 10, 0, sequences)
diffs = np.diff(prices, axis=1)
print(sequences)
print(prices)
print('part 1:', np.sum(sequences[:, 2000]))

# print(calc_score(prices, diffs, [-2, 1, -1, 3]))
print(find_best_seq(list(prices), list(diffs)))
# print({n: hash_n(n, 2000) for n in [1, 10, 100, 2024]})
# print('part 1:', sum(hash_n(int(seed), 2000) for seed in seeds))

print('----- test ---------')
seeds = np.array([123])
print(f'seeds: {seeds}')
sequences = hash_sequence(seeds, n_iterations=10)
print(f'sequences: {sequences}')
prices = np.apply_along_axis(lambda x: x % 10, 0, sequences)
print(f'prices: {prices}')
diffs = np.diff(prices, axis=1)
print(f'diffs: {diffs}')
for s, p, d in zip(sequences.tolist(), prices.tolist(), diffs.tolist()):
    for seq, price, diff in zip(s, p, d):
        print(f"{seq:8}: {price} ({diff:+})")
print(find_best_seq(prices, diffs))