import random
from itertools import product




class Hand:
    def __init__(self):
        self.cards = []
        self.card_values = []
        self.hand_value = 0
        self.soft = False


    def add(self, card):
        if card[0] == 'A':
            self.soft = True
        self.cards.append(card)

        value = self.get_card_value(card)
        self.card_values.append(value)

        self.update_hand_value(value)


    def get_card_value(self, card):
        d, s = card
        if d == 'A':
            return 11 if 21 - self.hand_value >= 11 else 1
        elif d in ['K', 'Q', 'J']:
            return 10
        else:
            return int(d)


    def update_hand_value(self, val):
        if self.hand_value + val > 21 and self.soft:
            for i, ((card, _), val) in enumerate(zip(self.cards, self.card_values)):
                if card == 'A':
                    self.card_values[i] = 1
            self.hand_value = sum(self.card_values)
        else:
            self.hand_value += val




class Deck:
    DENOMS = ['A', 'K', 'Q', 'J'] + [str(i) for i in range(10, 1, -1)]
    SUITES = ['C', 'S', 'H', 'D']


    def __init__(self):
        self.cards = None
        self.shuffled = None
        self.reset()


    def draw(self):
        try:
            card = self.cards.pop()
        except IndexError:
            card = None

        return card


    def shuffle(self):
        random.shuffle(self.cards)
        self.shuffled = True


    def reset(self):
        self.cards = self._generate_cards()
        self.shuffled = False


    def _generate_cards(self):
        return [(d, s) for d, s in product(Deck.DENOMS, Deck.SUITES)]


    def __add__(self, other):
        self.cards = self.cards + other.cards

        return self


    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)


    def __mul__(self, other):
        self.cards = self.cards * other
        
        return self


    def __rmul__(self, other):
        return self.__mul__(other)


    def __len__(self):
        return len(self.cards)


    def __str__(self):
        out = []
        for d, s in self.cards:
            out.append(f"{d}{s}")
        
        return ",".join(out)

