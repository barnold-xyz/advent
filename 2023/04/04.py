
cards = []

with open('04/input.txt', 'r') as file:
    for line in file:
        line = line.strip().split(':')
        card_number = line[0].strip().split()[1]
        line = line[1].split('|')
        cards.append({
            'card_number': card_number,
            'count': 1,
            'winners': line[0].strip().split(),
            'player_numbers': line[1].strip().split()
        })

def count_matchers(card):
    return len(set(card['player_numbers']).intersection(card['winners']))

def calc_value(card):
    num_matchers = count_matchers(card)
    if(num_matchers == 0):
        return 0
    return 2**((num_matchers)-1)

def summarize_part1():
    return sum([calc_value(card) for card in cards])

print(summarize_part1())

def score_one_card(card, deck):
    card_number = int(card['card_number'])
    card_count = int(card['count'])

    num_matchers = count_matchers(card)
    while num_matchers > 0:
        deck[(card_number-1) + num_matchers]['count'] += card_count
        num_matchers -= 1
    return deck

def score_deck(deck):
    for card in deck:
        score_one_card(card, deck)
    return deck

def summarize_part2():
    return sum([card['count'] for card in cards])

score_deck(cards)
print(summarize_part2())
