import random

class Card:
    def __init__(self, value):
        self.value = value

    def get_value(self):
        if self.value in ['J', 'Q', 'K']:
            return 10
        elif self.value == 'A':
            return 11
        else:
            return int(self.value)

    def __str__(self):
        return self.value

class Deck:
    def __init__(self):
        self.cards = [Card(val) for val in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']] * 4

    def deal_card(self):
        return self.cards.pop(random.randint(0, len(self.cards) - 1))

    def show_deck(self):
        return ', '.join(str(card) for card in self.cards)
    
class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        value = sum(card.get_value() for card in self.cards)
        aces = sum(1 for card in self.cards if card.value == 'A')
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    def __str__(self):
        return ', '.join([card.value for card in self.cards])
