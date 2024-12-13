sacks = open('2022/03/input.txt').read().strip().split('\n')

def score_letter(letter):
    return (ord(letter.upper()) - 64) + letter.isupper()*26

def dupes(sack):
    letter = max(set(list(sack[0:len(sack)//2])) & set(list(sack[len(sack)//2:])))
    return score_letter(letter)

def badges(sacks):
    return sum(score_letter(max(set(sacks[i]) & set(sacks[i+1]) & set(sacks[i+2]))) 
               for i in range(0, len(sacks), 3))

print('part 1:', sum(dupes(sack) for sack in sacks))
print('part 2:', badges(sacks))