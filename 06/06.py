import numpy as np

#epsilon = np.finfo(np.float64).tiny
epsilon = 1e-6

with open('06/input.txt', 'r') as file:
    input_data = file.readlines()

# have to determine how long to hold the button
# each 1s hold adds 1 mm/ms speed, but uses 1s of time
# distance = time * speed 
# distance = (time - hold) * hold
# want to find hold where record = (time - hold) * hold
# solved by quadratic equation: a = -1, b = time, c = -record
def ways_to_beat_record(time, record_dist):
    roots = np.roots([-1, time, -(record_dist+epsilon)])  # add an epsilon to beat the record, not tie
    return np.floor(max(roots)) - np.ceil(min(roots)) + 1

def summarize_part1(input_data):
    time_data = list(map(int, input_data[0].strip().split()[1:]))
    record_dist_data = list(map(int, input_data[1].strip().split()[1:]))
    solutions = [ways_to_beat_record(time, dist) for time, dist in zip(time_data, record_dist_data)]
    return int(np.cumulative_prod(solutions)[-1])

def summarize_part2(input_data):
    time =        int(input_data[0].strip().split(':')[1].replace(' ',''))
    record_dist = int(input_data[1].strip().split(':')[1].replace(' ',''))
    solutions = ways_to_beat_record(time, record_dist)
    return int(solutions)


print(summarize_part1(input_data))
print(summarize_part2(input_data))