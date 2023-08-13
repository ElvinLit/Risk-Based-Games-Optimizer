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
            return 11
        else:
            return int(self.value)

    def __str__(self):
        """Returns the string representation of the card's value."""
        return self.value


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
        """Removes and returns a random card from the deck."""
        return self.cards.pop(random.randint(0, len(self.cards) - 1))

    def show_deck(self):
        """Returns a string representation of all the cards in the deck."""
        return ', '.join(str(card) for card in self.cards)
    

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
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value
    
    def is_soft_hand(self):
        """Returns whether the hand is soft (contains an Ace counted as 11)."""
        value = sum(card.get_value() for card in self.cards)
        return value <= 21 and any(card.value == 'A' for card in self.cards)

    def __str__(self):
        """Returns the string representation of the cards in the hand."""
        return ', '.join([card.value for card in self.cards])


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
        if value in [2, 3, 4, 5, 6]:
            self.running_count += 1
        elif value in [10, 11]: # '10', 'J', 'Q', 'K', 'A'
            self.running_count -= 1

    def halves(self, card):
        """Updates the count using the Halves system."""
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
        """Updates the count using the Zen system."""
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

    def lose(self):
        """No action required as the bet has already been placed."""
        pass

    def draw(self):
        """Returns the bet to the bankroll."""
        self.bankroll += self.bet_size

    def get_bankroll(self):
        """Returns the current bankroll."""
        return self.bankroll

    def set_bet_size(self, bet_size):
        """Sets the bet size for the next hand."""
        self.bet_size = bet_size


def hit_or_stand(player_hand, dealer_upcard, count):
    """
    Follows basic strategy chart integrated with illustrious 18

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

    ### Illustrious 18 defined
    action = illustrious_18(player_value, dealer_value, count)
    if action is not None:
        return action

    ### Basic Strategy continues if nothing satisfies illustrious 18 

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


def illustrious_18(player_value, dealer_value, count):
    """
    Defines illustrious 18 combinations
    Args:
        player_value (int): value of the player's cards
        dealer_value (int): value of the dealer's cards
        count (int): running count
    Returns:
        None, True, or False, represents an action with True being to hit, False being to stand, and None being none of the conditions being met
    """
    
    # (player_value, dealer_value, count, action, operator)
    rules = [
        (16, 10, 0, False, '>='),
        (15, 10, 4, False, '>='),
        (10, 10, 3, True, '>='),
        (12, 3, 3, False, '>='),
        (12, 2, 4, False, '>='),
        (9, 2, 1, True, '>='),
        (9, 7, 4, True, '>='),
        (16, 9, 5, False, '>='),
        (13, 2, 0, True, '<='),
        (12, 4, 1, True, '<='),
        (12, 5, 0, True, '<='),
        (13, 3, -1, True, '<='),
    ]

    # Check if the current situation matches any rule
    for rule in rules:
        player_val, dealer_val, rule_count, action, comparison = rule
        if player_value == player_val and dealer_value == dealer_val:
            if comparison == '>=' and count >= rule_count:
                return action
            elif comparison == '<=' and count <= rule_count:
                return action

    # If no rule matches, return None to indicate no special action
    return None

def double_down(player_value, dealer_value, count):
    """
    Defines scenarios to double down on a bet
    Args:
        player_value (int): value of the player's cards
        dealer_value (int): value of the dealer's upcard
        count (int): running count
    Returns:
        None, True, represents an action with True being to double down
    """
    rules = [
        (10, 10, 3),
        (10, 10, 4),
        (9, 2, 1),
        (9, 7, 4)
    ]

    # Check rules
    for rule in rules:
        player_val, dealer_val, rule_count = rule
        if player_value == player_val and dealer_value == dealer_val and count == rule_count:
            return True
        
    # If no rule matches, return None to indicate no special action
    return None