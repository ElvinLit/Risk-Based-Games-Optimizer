import random

class Card:
    """
    Represents a playing card.

    Attributes:
        value (str): The value of the card.

    Methods:
        get_value: Returns the integer value of the card.
        __str__: Returns the string representation of the card.
    """

    def __init__(self, value):
        """Initialize a Card object with a given value."""
        self.value = value

    def get_value(self):
        """Returns the integer value of the card."""
        if self.value in ['J', 'Q', 'K']:
            return 10
        elif self.value == 'A':
            return 1
        else:
            return int(self.value)
    def __str__(self):
        return f"{self.value}"


class Deck:
    """
    Represents a deck of playing cards.

    Attributes:
        cards (list): A list of Card objects.

    Methods:
        deal_card: Removes and returns a random card from the deck.
        show_deck: Returns a string representation of all the cards in the deck.
    """
    def __init__(self):
        """Initialize a Deck object with 52 shuffled cards."""
        self.cards = [Card(val) for val in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']] * 4
        random.shuffle(self.cards)

    def deal_card(self):
        """Removes and returns the top card from the deck."""
        return self.cards.pop()
    

class Hand:
    """
    Represents a hand of playing cards.

    Attributes:
        cards (list): A list of Card objects.

    Methods:
        add_card: Adds a Card object to the hand.
        get_value: Returns the total value of the cards in the hand.
        is_soft_hand: Returns whether the hand is soft (contains an Ace counted as 11).
        __str__: Returns the string representation of the cards in the hand.
    """

    def __init__(self):
        """Initialize a Hand object with an empty list."""
        self.cards = []

    def add_card(self, card):
        """Adds a Card object to the hand."""
        self.cards.append(card)

    def get_value(self):
        """Returns the total value of the cards in the hand."""
        value = sum(card.get_value() for card in self.cards)
        aces = sum(1 for card in self.cards if card.value == 'A')
        if aces > 0 and value + 10 <= 21:
            value += 10
        return value
    
    def is_soft_hand(self):
        """Returns whether the hand is soft (contains an Ace counted as 11)."""
        value_without_ace = sum(card.get_value() for card in self.cards if card.value != 'A')
        aces_count = sum(1 for card in self.cards if card.value == 'A')
        return aces_count > 0 and (value_without_ace + aces_count * 11) <= 21
    
    def get_cards(self):
        """Returns a list of the string representations of the cards in the hand."""
        return [str(card) for card in self.cards]
    
    def __str__(self):
        return f"{self.value}"


class CardCounter:
    """
    Represents a card counter using different counting systems.

    Attributes:
        running_count (int): The current running count.

    Methods:
        high_low: Updates the count using the Hi-Lo system.
        halves: Updates the count using the Halves system.
        zen: Updates the count using the Zen system.
        get_running_count: Returns the current running count.
        reset_count: Resets the running count to 0.
    """

    def __init__(self):
        """Initialize a CardCounter object with a running count of 0."""
        self.running_count = 0

    def high_low(self, card):
        """Updates the count using the Hi-Lo system."""
        value = card.get_value()
        if card.value == 'A':
            self.running_count -= 1
        elif value in [2, 3, 4, 5, 6]:
            self.running_count += 1
        elif value in [10]: # '10', 'J', 'Q', 'K'
            self.running_count -= 1

    def halves(self, card):
        """Updates the count using the Halves system."""
        if card.value == '2':
            self.running_count += 0.5
        elif card.value in ['3', '4', '6']:
            self.running_count += 1
        elif card.value == '5':
            self.running_count += 1.5
        elif card.value == '7':
            self.running_count += 0.5
        elif card.value == '9':
            self.running_count -= 0.5
        elif card.value in ['10', 'J', 'Q', 'K', 'A']:
            self.running_count -= 1

    def zen(self, card):
        """Updates the count using the Zen system."""
        if card.value in ['2', '3', '7']:
            self.running_count += 1
        elif card.value in ['4', '5', '6']:
            self.running_count += 2
        elif card.value in ['10', 'J', 'Q', 'K']:
            self.running_count -= 2
        elif card.value == 'A':
            self.running_count -= 1

    def get_running_count(self):
        """Returns the current running count."""
        return self.running_count

    def reset_count(self):
        """Resets the running count to 0."""
        self.running_count = 0


class Player:
    """
    Represents a player in the blackjack game.

    Attributes:
        bankroll (float): The current amount of money the player has.
        bet_size (float): The current bet size.

    Methods:
        place_bet: Places a bet and deducts the amount from the bankroll.
        win: Adds the bet amount to the bankroll.
        lose: No action required as the bet has already been placed.
        draw: Returns the bet to the bankroll.
        get_bankroll: Returns the current bankroll.
        set_bet_size: Sets the bet size for the next hand.
    """

    def __init__(self, starting_bankroll):
        """Initialize a Player object with a given bankroll."""
        self.bankroll = starting_bankroll
        self.bet_size = 0

    def place_bet(self, bet_size):
        """Places a bet and deducts the amount from the bankroll."""
        self.bet_size = bet_size
        self.bankroll -= bet_size

    def win(self):
        """Adds the bet amount to the bankroll."""
        self.bankroll += self.bet_size * 2
        
    def blackjack(self):
        self.bankroll += (self.bet_size * 2) + (self.bet_size * 3/2)

    def lose(self):
        """No action required as the bet has already been placed."""
        pass
    
    def split(self, bet_size):
        """Splits the current bet into two hands."""
        self.bankroll -= bet_size
        self.bet_size *= 2

    def draw(self):
        """Returns the bet to the bankroll."""
        self.bankroll += self.bet_size

    def get_bankroll(self):
        """Returns the current bankroll."""
        return self.bankroll

    def set_bet_size(self, bet_size):
        """Sets the bet size for the next hand."""
        self.bet_size = bet_size
        

def should_split(player_hand, dealer_up_card, count):
    """Returns True if the player should split the hand."""
    if len(player_hand.cards) != 2 or player_hand.cards[0].value != player_hand.cards[1].value:
        return False

    pair_value = player_hand.cards[0].value
    dealer_value = dealer_up_card.get_value()

    if pair_value == 'A':
        return True
    
    if pair_value in ['J', 'Q', 'K']:
        if (dealer_value == 6) and (count >= 4):
            return True
        if (dealer_value == 5) and (count >= 5):
            return True
        if (dealer_value == 4) and (count >= 6):
            return True
        return False
    
    if pair_value == '9':
        if dealer_up_card.value in ['7', '10', 'A']:
            return False
        return True
    
    if pair_value == '8':
        return True
    
    if pair_value in ['7', '3', '2']:
        if dealer_up_card.value in ['8', '9', '10', 'A']:
            return False
        return True
    
    if pair_value == '6':
        if dealer_up_card.value in ['7', '8', '9', '10', 'A']:
            return False
        return True
            
    if pair_value == '5':
        return False
    
    if pair_value == '4':
        if dealer_up_card.value in ['5', '6']:
            return True
        return False
    
    return False

def should_insurance(count):
    """Returns True or False on if one should surrender"""
    if count >= 3:
        return True
    return False

def should_surrender(player_hand, dealer_up_card, count):
    """Returns True or False on if one should surrender"""
    player_value = player_hand.get_value()
    dealer_value = dealer_up_card.get_value()
    
    if player_value == 17:
        if dealer_up_card.value == 'A':
            return True
    if player_value == 16:
        if dealer_up_card.value in ['10', 'A']:
            return True
        if dealer_up_card.value == '9':
            if count > 1:
                return True
        if dealer_up_card.value == '8':
            if count >= 4:
                return True
        return False
    if player_value == 15:
        if dealer_up_card.value == '9':
            if count >= 2:
                return True
        if dealer_up_card.value == '10':
            if count > 0:
                return True
        if dealer_up_card.value == 'A':
            if count < 1:
                return True
        return False


def split_hands(hand):
    """Splits a hand into two new hands."""
    new_hand1 = Hand()
    new_hand2 = Hand()
    new_hand1.add_card(hand.cards.pop(0))
    new_hand2.add_card(hand.cards.pop(0))
    return new_hand1, new_hand2


def hit_or_stand(player_hand, dealer_upcard, count):
    """
    Follows basic strategy chart integrated with illustrious 18, utilizes player and, dealer upcard, and the count to determine hit or stand

    Args:
        player_hand (Hand obj)
        dealer_upcard (Card Obj)
        count(int)

    Returns:
        boolean: True if we should hit, False to stand
    """

    player_value = player_hand.get_value()
    dealer_value = dealer_upcard.get_value()
    soft_hand = player_hand.is_soft_hand()

    # Checks soft hand cases (Ace is present)
    if soft_hand:
        # Hit combinations
        if '9' in player_hand.get_cards():
            return False
        
        if '8' in player_hand.get_cards():
            if (dealer_upcard.value == '4') and (count >= 3):
                return True
            elif (dealer_upcard.value in ['5', '6']) and (count >= 1):
                return True
            return False
        
        if '7' in player_hand.get_cards():
            return dealer_upcard.value not in ['7', '8']
        
        if '6' in player_hand.get_cards():
            return (dealer_upcard.value != '2') or (count < 1)
        return True

    # Cases when player value <= 11
    if player_value <= 11:
        if (player_value == 11) and (dealer_upcard.value == 'A') and (count >= 1):
            return False
        if (player_value == 10) and (dealer_upcard.value in ['10', 'A']) and (count >= 4):
            return False
        if (player_value == 9):
            if (dealer_upcard.value == '2') and count >= 1:
                return False
            if (dealer_upcard.value == '7') and count >= 3:
                return False
        if (player_value == 8) and (dealer_upcard.value == '6') and (count >= 2):
                return False
        return True
    
    # Special cases for 12-16
    if 12 <= player_value <= 16:
        
        if player_value == 12:        
            if dealer_upcard.value == '2' and count >= 3:
                return False
            if dealer_upcard.value == '3' and count >= 2:
                return False
            if dealer_upcard.value == '4' and count <= 0:
                return True
            if dealer_upcard.value in ['5', '6']:
                return False
            return True
        
        if player_value == 13:
            if dealer_upcard.value == '2' and count <= 1:
                return True
            if dealer_upcard.value in ['3','4','5','6']:
                return False
            return True
        
        if player_value == 14:
            if dealer_upcard.value in ['2','3','4','5','6']:
                return False
            return True
        
        if player_value == 15:
            if dealer_upcard.value in ['2','3','4','5','6']:
                return False
            else:
                if (dealer_upcard.value == '10') and (count >= 4):
                    return False
                return True
        
        if player_value == 16:
            if dealer_upcard.value in ['2','3','4','5','6']:
                return False
            else:
                if (dealer_upcard.value == '9') and (count >= 4):
                    return False
                if (dealer_upcard.value == '10') and (count >= 0):
                    return False
                return True
                    
    # Stand on 17+
    return False


def double_down(player_hand, dealer_upcard, count):
    player_value = player_hand.get_value()
    dealer_value = dealer_upcard.get_value()
    
    rules = [
        (10, 10, 3),
        (10, 10, 4),
        (9, 2, 1),
        (9, 7, 4)
    ]

    # Check rules
    for rule in rules:
        player_val, dealer_val, rule_count = rule
        if player_value == player_val and dealer_value == dealer_val and count >= rule_count:  # Compare count with rule_count
            return True
        
    # If no rule matches, return False to indicate no special action
    return False