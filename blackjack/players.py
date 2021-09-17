


class BJDealer:
    def __init__(self):
        self.hand = []
        self.hand_value = 0
        self.soft = False

    def hit(self, shoe):
        card = shoe.pop()
        self.hand.append(card)
        denoms = self.get_hand_denoms()
        if 'A' in denoms:
            hv = 0
            num_aces = 0
            for denom in denoms:
                if denom == 'A':
                    num_aces += 1
                else:
                    hv += 10 if denom in ['K', 'Q', 'J'] else int(denom)
            
            for _ in range(num_aces):
                hv += 1 if hv > 10 else 11
            self.hand_value = hv
        else:
            denom = card[0]
            self.hand_value += 10 if denom in ['K', 'Q', 'J'] else int(denom)

        return shoe
        '''    
        denoms = sorted(self.get_hand_denoms())
        if 'A' in denoms:
            hv = 0
            for denom in denoms:
                if denom == 'A':
                    hv += 1 if hv > 10 else 11
                elif denom in ['K', 'Q', 'J']:
                    hv += 10
                else:
                    hv += int(denom)
            self.hand_value = hv
        else:
            denom = card[0]
            self.hand_value += 10 if denom in ['K', 'Q', 'J'] else int(denom)
        '''

        '''
        denom = card[0]
        if denom == 'A':
            if self.hand_value > 10:
                self.hand_value += 1
            else:
                self.hand_value += 11
                self.soft = True
        elif denom in ['K', 'Q', 'J']:
            self.hand_value += 10
        else:
            self.hand_value += int(denom)
        '''

    def reset_hand(self):
        self.hand = []
        self.hand_value = 0

    def get_showing_card(self):
        return self.hand[1][0]

    def get_hand_denoms(self):
        return [c[0] for c in self.hand]
    
    def show_hand(self):
        print(self.get_hand_denoms())

    def show_hand_value(self):
        print(self.hand_value)

    def hand_summary(self):
        print(f'Hand: {self.get_hand_denoms()}')
        print(f'Value: {self.hand_value}')




class BJPlayer(BJDealer):
    def __init__(self, bank_roll):
        super().__init__()
        self.bank_roll = bank_roll

    def update_bank_roll(self, amt):
        if self.bank_roll + amt < 0:
            return False
        else:
            self.bank_roll += amt
        
        return True
