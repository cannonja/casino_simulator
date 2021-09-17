from itertools import product
import random
from players import BJDealer, BJPlayer

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
dealer = BJDealer()
players = {f'p{i}': BJPlayer(100) for i in range(1, NUM_PLAYERS + 1)}

for _ in range(2):
    for p in players:
        ret = players[p].update_bank_roll(-10)
        if ret == True:
            shoe = players[p].hit(shoe)
    shoe = dealer.hit(shoe)

### Play
# Dealer has black jack
if dealer.hand_value == 21:
    for p in players:
        if players[p].hand_value == 21:
            players[p].update_bank_roll(10)
else:
    # Check for players with blackjack
    for p in players:
        if players[p].hand_value == 21:
            players[p].update_bank_roll(10)



            

# Players have black jack

# Player moves
#basic_strategy(player, dealer_card, shoe)
#no_bust_strategy(player, dealer_card, shoe)

# Dealer moves
#dealer_strategy(dealer, shoe)

