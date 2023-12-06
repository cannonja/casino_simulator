from cards import Hand


class BJPlayer:
    def __init__(self, bet=10, bank_roll=None, strategy=None):
        self.hands = None
        self.hand = None
        self.hand_committed = None
        self.active = None
        self.reset_hand()
        self.strategy = 'dealer' if strategy is None else strategy
        self._bet = bet
        self.bet = bet
        self.bank_roll = bank_roll
        self.history = None
        self.history_committed = None
        self.reset_history()
    

    def reset_bet(self, bet=None):
        if bet is None:
            self.bet = self._bet
        else:
            self.bet = bet

    
    def place_bet(self, bet=None):
        if bet is None:
            bet = self.bet
        else:
            self.bet = bet
        self.update_bank_roll(-bet)


    def win_bet(self, bet=None):
        if bet is None:
            bet = self.bet
        self.update_bank_roll(bet)

    
    def play(self, shoe, dealer_card):
        if self.strategy == 'no_bust':
            self._no_bust(shoe)
        elif self.strategy == 'dealer':
            self._dealer(shoe)


    def _no_bust(self, shoe):
        while self.active:
            if self.hand.hand_value < 12:
                self.hit(shoe)
                if self.hand.busted:
                    self.deactivate()
            else:
                # Stay
                self.deactivate()


    def _dealer(self, shoe):
        while self.active:
            if self.hand.hand_value < 17:
                self.hit(shoe)
                if self.hand.busted:
                    self.deactivate()
            else:
                self.deactivate()

    
    def commit_win(self):
        self._commit('win')

    
    def commit_loss(self):
        self._commit('loss')


    def commit_push(self):
        self._commit('push')


    def _commit(self, result):
        self.history['hands'].extend(self.hands)
        self.history['bets'].append(self.bet)
        self.history['bank_roll'].append(self.bank_roll)
        self.history['results'].append(result)
        self.hand_committed = True

    
    def hit(self, shoe):
        card = shoe.draw()
        self.hand.add(card)

    
    def update_bank_roll(self, amt):
        self.bank_roll += amt


    def activate(self):
        self.active = True

    
    def deactivate(self):
        self.active = False


    def reset_hand(self):
        self.hands = [Hand()]
        self.hand = self.hands[0]
        self.hand_committed = False
        self.activate()


    def reset_history(self):
        self.history = {
            'hands': [],
            'bets': [],
            'bank_roll': [],
            'results': []
            }

    
    def hand_summary(self):
        print(f'Hand: {self.get_hand_denoms()}')
        print(f'Value: {self.hand_value}')




class BJDealer(BJPlayer):
    def __init__(self):
        super().__init__()

    
    def get_showing_card(self):
        return self.hand.cards[1][0]


    def play(self, shoe):
        self._dealer(shoe)
