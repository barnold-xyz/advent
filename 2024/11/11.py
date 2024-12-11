data = '125 17'
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

def test(stones):
    print(f'0: {stones}')
    for i in range(1, 25+1):
        stones = blink(stones)
        if i <= 6:
            print(f'{i}: {stones}')
        if i == 6: 
            print(len(stones))
    print(len(stones))


test(stones)