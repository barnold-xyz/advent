
cards = []

with open('04/input.txt', 'r') as file:
    for line in file:
        line = line.strip().split(':')[1] # Remove the card number
        line = line.split('|')
        cards.append({
            'winners': line[0].strip().split(),
            'player_numbers': line[1].strip().split()
        })

def calc_value(card):
    matchers = set(card['player_numbers']).intersection(card['winners'])
    if(len(matchers) == 0):
        return 0
    return 2**(len(matchers)-1)

def summarize_part1():
    return sum([calc_value(card) for card in cards])

print(summarize_part1())





#''' debug

#'''