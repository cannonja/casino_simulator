from cards import Hand


class BJPlayer:
    def __init__(self, bank_roll=None, strategy=None):
        self.hands = None
        self.hand = None
        self.reset_hand()
        self.strategy = 'dealer' if strategy is None else strategy
        self.bank_roll = bank_roll
        self.active = True

    
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

    
    def hand_summary(self):
        print(f'Hand: {self.get_hand_denoms()}')
        print(f'Value: {self.hand_value}')




class BJDealer(BJPlayer):
    def __init__(self):
        super().__init__()

    def get_showing_card(self):
        return self.hand.cards[1][0]
