from itertools import product
import random

### Build shoe and shuffle
NUM_DECKS = 2
denoms = ['A', 'K', 'Q', 'J'] + [str(i) for i in range(10, 1, -1)]
suites = ['c', 's', 'h', 'd']
deck = [f'{d}{s}' for d, s in product(denoms, suites)]
shoe = deck * NUM_DECKS
for _ in range(4):
    random.shuffle(shoe)

### Deal initial hand
NUM_PLAYERS = 3
dealer = []
players = {f'p{i}': [] for i in range(1, NUM_PLAYERS + 1)}

for _ in range(2):
    for p in players:
        players[p].append(shoe.pop()[0])
    dealer.append(shoe.pop()[0])

### Play
# Dealer has black jack

# Players have blackjack

# Player moves
#basic_strategy(player_hand, dealer_card, shoe)
#no_bust_strategy(player_hand, dealer_card, shoe)

# Dealer moves
#dealer_strategy(dealer_hand, shoe)

