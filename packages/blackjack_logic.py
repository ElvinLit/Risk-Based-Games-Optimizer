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
        random.shuffle(self.cards)

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
    
    def is_soft_hand(self):
        # Check if the hand is soft (contains an ace counted as 11)
        value = sum(card.get_value() for card in self.cards)
        return value <= 21 and any(card.value == 'A' for card in self.cards)

    def __str__(self):
        return ', '.join([card.value for card in self.cards])


class CardCounter:
    def __init__(self):
        self.running_count = 0

    def high_low(self, card):
        value = card.get_value()
        if value in [2, 3, 4, 5, 6]:
            self.running_count += 1
        elif value in [10, 11]: # '10', 'J', 'Q', 'K', 'A'
            self.running_count -= 1

    def halves(self, card):
        value = card.get_value()
        if value == 2:
            self.running_count += 0.5
        elif value == 3 or value == 4 or value == 6:
            self.running_count += 1
        elif value == 5:
            self.running_count += 1.5
        elif value == 7:
            self.running_count += 0.5
        elif value == 9:
            self.running_count -= 0.5
        elif value in [10, 11]: # '10', 'J', 'Q', 'K', 'A'
            self.running_count -= 1
    
    def zen(self, card):
        value = card.get_value()
        if value in [2, 3, 7]:
            self.running_count += 1
        elif value in [4, 5, 6]:
            self.running_count += 2
        elif value in [10, 11]: # '10', 'J', 'Q', 'K', 'A'
            if card.value == 'A':
                self.running_count -= 1
            else:
                self.running_count -= 2

    def get_running_count(self):
        return self.running_count

    def reset_count(self):
        self.running_count = 0

def basic_strategy(player_hand, dealer_upcard):
    """
    Follows basic strategy chart

    Args:
        player_hand (Hand obj)
        dealer_upcard (Card Obj)

    Returns:
        boolean: True if we should hit, False to stay
    """
    player_value = player_hand.get_value()
    dealer_value = dealer_upcard.get_value()
    soft_hand = player_hand.is_soft_hand()

    # Hit on <= 11
    if player_value <= 11:
        return True
    
    # Checks soft hand case (Ace)
    if soft_hand:
        if player_value == 18:
            return dealer_value in [9, 10, 11]
        return player_value < 18

    # Special cases for 12-16
    if 12 <= player_value <= 16:
        if 2 <= dealer_value <= 6:
            return False
        else: 
            return True
        
    # Stand on 17+
    return False