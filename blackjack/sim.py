from itertools import product
import random
from players import BJDealer, BJPlayer
from cards import Hand, Deck
import pandas as pd




def play_round(dealer, players, shoe):
    if len(shoe) < 20:
        return "Round aborted, reached end of shoe"

    # Place bets
    dealer.activate()
    for p in players:
        players[p].activate()
        players[p].place_bet()

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
                players[p].win_bet()
                players[p].commit_push()
    else:
        # Payout players with blackjack
        # Deactivate these players
        for p in players:
            if players[p].hand.hand_value == 21:
                players[p].deactivate()
                players[p].win_bet(players[p].bet * 2.5)
                players[p].commit_win()

    # Play with remaining active players
    if sum([p.active for _, p in players.items()]) > 0:
        # Player moves - no bust
        player_bet = BET
        dealer_card = dealer.get_showing_card()
        for p in players:
            players[p].play(shoe, dealer_card)
            '''
            if players[p].active:
                staying = False
                while not staying and not players[p].hand.busted:
                    if players[p].hand.hand_value < 12:
                        players[p].hit(shoe)
                    else:
                        staying = True
            '''

        # Dealer moves - stand on soft 17
        dealer.play(shoe)
        '''
        staying = False
        while not staying and not dealer.hand.busted:
            if dealer.hand.hand_value > 16:
                staying = True
            else:
                dealer.hit(shoe)
        '''

    # Score 
    for p in players:
        if not players[p].hand_committed:
            if players[p].hand.busted:
                # Busted
                players[p].commit_loss()
            elif players[p].hand.hand_value > dealer.hand.hand_value or dealer.hand.busted:
                # Won
                players[p].win_bet(players[p].bet * 2)
                players[p].commit_win()
            elif players[p].hand.hand_value == dealer.hand.hand_value:
                # Push
                players[p].win_bet()
                players[p].commit_push()
            else:
                # Not busted, but didn't beat the dealer
                players[p].commit_loss()


    '''
    # Print Results
    print(dealer.hand)
    print()

    for _, p in players.items():
        print(p.hand)
        print(f"Bank Roll: {p.bank_roll}")
        print()
    '''



def build_shoe(num_decks):
    shoe = Deck() * num_decks
    for _ in range(4):
        shoe.shuffle()

    return shoe




if __name__ == '__main__':
    ### Build shoe and shuffle
    NUM_DECKS = 6
    shoe = build_shoe(NUM_DECKS)

    ### Initialize players
    BET = 10
    NUM_PLAYERS = 1
    dealer = BJDealer()
    players = {f'p{i + 1}': BJPlayer(bet=BET, bank_roll=300, strategy='no_bust') for i in range(NUM_PLAYERS)}

    ### Run simulation
    NUM_HANDS = 100000
    for _ in range(NUM_HANDS):
        if len(shoe) < 20:
            shoe = build_shoe(NUM_DECKS)
        play_round(dealer, players, shoe)

        # Reset hands
        dealer.reset_hand()
        for p in players:
            players[p].reset_hand()

        # Update bets if needed (Martingale)
        for p in players:
            last_result = players[p].history['results'][-1]
            last_bet = players[p].bet
            if last_result == 'loss':
                players[p].reset_bet(last_bet * 2)
            elif last_result == 'win':
                players[p].reset_bet()

    '''
    ### View history
    for p in players:
        print(players[p].history['results'])
        print(players[p].history['bank_roll'])
        print()
    '''
    results = players['p1'].history['results']
    i = -1
    last = None
    streaks = []
    for r in results:
        if r != last:
            i += 1
        last = r
        streaks.append(i)
    sdf = pd.DataFrame({'streak': streaks, 'result': results})
    loss_dist = sdf.groupby(['streak', 'result'], as_index=False) \
                   .size() \
                   .query("result == 'loss'") \
                   .groupby(['result', 'size']) \
                   .size() \
                   .transform(lambda x: x / x.sum())
    print(loss_dist.cumsum())



    












#basic_strategy(player, dealer_card, shoe)
#no_bust_strategy(player, dealer_card, shoe)

# Dealer moves
#dealer_strategy(dealer, shoe)

