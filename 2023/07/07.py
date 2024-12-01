plays = []
with open('07/input.txt', 'r') as file:
    for line in file:
        plays.append(line.strip().split())

def hand_waterfall(hand, jokers_wild=False): 
    num_jokers = hand.count('J') if jokers_wild else 0
    if(num_jokers >= 4): return 1e7
    #print ('num_jokers:', num_jokers)
    for char in set(hand):
        if jokers_wild and (char == 'J'): continue
        if hand.count(char) == 5 - num_jokers:
            return 1e7
        if hand.count(char) == 4 - num_jokers:
            return 1e6
        
    # not a five of a kind or four of a kind, check for full house
    # if there are 3 or more jokers, the hand is 4oak or better
    for char in set(hand):
        if num_jokers == 2:
            return 1e4 # has to be a 3OAK, can't have a full house w/ 2 jokers (it would be 4OAK)
        elif num_jokers == 1:
            if hand_waterfall(hand.replace('J',''), False) == 1e3:  # if the rest of the hand is 2 pair, then this is a full house
                return 1e5
            elif hand_waterfall(hand.replace('J',''), False) == 1e2: # pair turns into 3OAK
                return 1e4
            else: 
                return 1e2 # worst case is a pair
        elif hand.count(char) == 3:  # the zero joker case
            #print('here', hand) 
            for char2 in set(hand):
                if hand.count(char2) == 2: 
                    return 1e5
            # not a full house so must be three of a kind
            return 1e4
    
    # only possibilities are two pair, one pair, or high card
    for char in set(hand):
        if hand.count(char) == 2 - num_jokers:
            for char2 in set(hand):
                if hand.count(char2) == 2 and char != char2: ## TODO: deal with jokers here too?
                    return 1e3
            return 1e2
    return 1e1

def cards2hex(hand, jokers_wild=False):
    card_to_hex_map = {
        'T': 'A',
        'J': 'B',
        'Q': 'C',
        'K': 'D',
        'A': 'E'
    }
    if jokers_wild: card_to_hex_map['J'] = '0'

    hex_hand = ''
    for char in hand:
        if char in card_to_hex_map:
            hex_hand += card_to_hex_map[char]
        else:
            hex_hand += char
    return hex_hand

def hand_value(hand, jokers_wild=False):
    type_value = int(hand_waterfall(hand, jokers_wild))
    cards_value = cards2hex(hand, jokers_wild)
    combined_value = str(type_value) + cards_value
    hex_value = int(combined_value, 16)
    #hex_value = hex(int(combined_value, 16))
    return hex_value

def summarize(plays, jokers_wild):
    # add the values of each hand
    plays = [(hand, int(bid), hand_value(hand, jokers_wild)) for (hand, bid) in plays]

    # sort the plays by value and rank them
    plays = sorted(plays, key=lambda x: x[2], reverse=False)
    plays = [(hand, bid, value, rank + 1) for (rank, (hand, bid, value)) in enumerate(plays)]
    return sum([bid * rank for (hand, bid, value, rank) in plays])

print(summarize(plays, jokers_wild=False))
print(summarize(plays, jokers_wild=True))

#print(hand_value('2345J', jokers_wild=True))
#print(hand_value('23455', jokers_wild=True))