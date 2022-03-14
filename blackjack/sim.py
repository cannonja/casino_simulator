from itertools import product
import random
from players import BJDealer, BJPlayer
from cards import Hand, Deck

### Build shoe and shuffle
NUM_DECKS = 2
shoe = Deck() * NUM_DECKS
for _ in range(4):
    shoe.shuffle()

### Play hand
BET = 10
NUM_PLAYERS = 3
dealer = BJDealer()
players = {f'p{i}': BJPlayer(100) for i in range(1, NUM_PLAYERS + 1)}

# Place bets
for p in players:
    players[p].update_bank_roll(-BET)

# Deal first two cards
for _ in range(2):
    for p in players:
        players[p].hit(shoe)
    dealer.hit(shoe)

# First check for dealer blackjack and continue hand if false (removing players as needed)
if dealer.hand.hand_value == 21:
    # Assume push if player also has blackjack
    # Deactivate all players since hand is over
    for p in players:
        players[p].deactivate()
        if players[p].hand.hand_value == 21:
            players[p].update_bank_roll(BET)
else:
    # Payout players with blackjack
    # Deactivate these players
    for p in players:
        if players[p].hand.hand_value == 21:
            players[p].deactivate()
            players[p].update_bank_roll(BET * 3)

if sum([p.active for _, p in players.items()]) > 0:
    # Player moves - no bust
    player_bet = BET
    dealer_card = dealer.get_showing_card()
    for p in players:
        staying = False
        while not staying and not players[p].hand.busted:
            if players[p].hand.hand_value < 12:
                players[p].hit(shoe)
            else:
                staying = True

    # Dealer moves - stand on soft 17
    staying = False
    while not staying and not dealer.hand.busted:
        if dealer.hand.hand_value > 16:
            staying = True
        else:
            dealer.hit(shoe)

# Score
for p in players:
    if not players[p].hand.busted:
        if players[p].hand.hand_value > dealer.hand.hand_value or dealer.hand.busted:
            players[p].update_bank_roll(BET * 2)
        elif players[p].hand.hand_value == dealer.hand.hand_value:
            players[p].update_bank_roll(BET)

print(dealer.hand)
print()

for _, p in players.items():
    print(p.hand)
    print(f"Bank Roll: {p.bank_roll}")
    print()









#basic_strategy(player, dealer_card, shoe)
#no_bust_strategy(player, dealer_card, shoe)

# Dealer moves
#dealer_strategy(dealer, shoe)

