import numpy as np
pattern = r'\d+'
dtype = [('', int)] * 6
print(f"Pattern: {pattern}, Dtype: {dtype}")

data = np.fromregex('2024/13/test.txt', pattern, dtype)
print(f"Data from file: {data}")

reshaped_data = data.view(int).reshape(-1, 3, 2)
print(f"Reshaped data: {reshaped_data}")

M = reshaped_data.swapaxes(1, 2)
print(f"Swapped axes data: {M}")

for p in 0, 1e13:
    S = M[..., :2]
    P = M[..., 2:] + p
    R = np.linalg.solve(S, P).round().astype(int)
    print(R)
    print(R.squeeze())
    print(*R.squeeze() @ [3,1] @ (S @ R == P).all(1))