import random
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

from packages.graphs import styling_configurations


"""
Contains all classes and methods for Blackjack strategy experimentation
"""

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


def blackjack_simulator(num_plays, starting_bankroll, base_bet, counting_strategy):
    """
    Simulates a Blackjack game using the high low counting strategy. 
    Args:
        num_plays (int): number of plays for the simulation
        starting_bankroll (float): starting amount of money for the player
        base_bet (float): base bet size
    Returns:
        DataFrame: contains information with columns ['Win', 'Loss', 'Draw','Running Count', 'Play Count']
    """

    deck = Deck()
    counter = CardCounter()
    player = Player(starting_bankroll)
    
    counting_method = getattr(counter, counting_strategy)
    
    df = pd.DataFrame(columns=['Win', 'Loss', 'Draw', 'Running Count', 'Play Count', 'Player Hand Value', 'Dealer Hand Value', 'Balance', 'Splitted', 'Doubled', 'First Card', 'Second Card', 'Dealer Upcard', 'Blackjack'])

    i = 0
    while i < num_plays:
        
        # New hands each round
        player_hand = Hand()
        dealer_hand = Hand()

        # Check for deck exhaustion 
        if len(deck.cards) < 15: # Arbitrary threshold
            deck = Deck() 
            counter.reset_count()

        # Set bet size 
        bet_size = base_bet 
        player.place_bet(bet_size)

        # Initial Dealing, 2 cards each, assume only the dealer's first card is shown to the player
        for j in range(2):
            player_card = deck.deal_card()
            dealer_card = deck.deal_card()

            player_hand.add_card(player_card)
            dealer_hand.add_card(dealer_card)

            counting_method(player_card)
            if j == 0:
                counting_method(dealer_card)
        
        if should_split(player_hand, dealer_hand.cards[0], counter.get_running_count()) == True:
            # Place second bet
            player.place_bet(bet_size)
            
            hand1, hand2 = split_hands(player_hand)
            # Play both hands separately, adjusting bets and counts for each
            
            # Play the dealer's hand 
            while dealer_hand.get_value() < 17:
                dealer_hand.add_card(deck.deal_card())
            
            for split_hand in [hand1, hand2]:
                
                # Initialize our row for the dataframe
                row = [0] * 14
                
                # Double initializer
                double_bool = False
                
                # Place the bet for the split hand
                split_bet = bet_size
                player.set_bet_size(split_bet)

                if double_down(split_hand, dealer_hand.cards[0], counter.get_running_count()) == True:
                    player.place_bet(split_bet)
                    player.set_bet_size(split_bet * 2)
                    
                    double_bool = True
                    row[9] = 1
           
                # Hit or Stand for splitted hand
                split_hand.add_card(deck.deal_card())
                while split_hand.get_value() < 21:
                    action = hit_or_stand(split_hand, dealer_hand.cards[0], counter.get_running_count())
                    if action:
                        new_card = deck.deal_card()
                        split_hand.add_card(new_card)
                        counting_method(new_card)
                    else:
                        break
                
                # Determine win/loss/draw
                if split_hand.get_value() > 21:
                    player.lose()
                    row[1] += 1
                elif ((split_hand.cards[0].value == "A") and (split_hand.cards[1].value in ['10','K','Q','J'])) or ((split_hand.cards[0].value in ['10','K','Q','J']) and (split_hand.cards[1].value == "A")):
                    player.blackjack()
                    row[0] += 1
                    row[13] += 1
                elif dealer_hand.get_value() > 21 or split_hand.get_value() > dealer_hand.get_value():
                    player.win()
                    row[0] += 1

                elif split_hand.get_value() == dealer_hand.get_value():
                    player.draw()
                    row[2] += 1
                else:
                    player.lose()
                    row[1] += 1
                
                # Player's Cards
                row[10] = str(split_hand.cards[0])
                row[11] = str(split_hand.cards[1])
                
                # Dealer's Upcard
                row[12] = str(dealer_hand.cards[0])
                
                # Play Count
                row[4] = i + 1
                # Running Count
                row[3] = counter.get_running_count()
                # Player Hand
                row[5] = split_hand.get_value()
                # Dealer Hand
                row[6] = dealer_hand.get_value()
                # Balance
                row[7] = player.get_bankroll()
                # Splitted
                row[8] = 1
                # Append row to dataframe
                df.loc[len(df)] = row
                i += 1
        
        else:
            # Initialize our row for the dataframe
            row = [0] * 14
            # Double initializer
            double_bool = False
            
            # Double bet if applicable
            if double_down(player_hand, dealer_hand.cards[0], counter.get_running_count()) == True:
                player.place_bet(bet_size)
                player.set_bet_size(bet_size * 2)
                row[9] = 1
                double_bool = True
            
            # Deal one more card if doubled down
            if double_bool == True:
                double_new_card = deck.deal_card()
                player_hand.add_card(double_new_card)
                counting_method(double_new_card)
            
            # Hit or Stand
            while (player_hand.get_value() < 21) and (double_bool == False):
                action = hit_or_stand(player_hand, dealer_hand.cards[0], counter.get_running_count())
                if action:
                    new_card = deck.deal_card()
                    player_hand.add_card(new_card)
                    counting_method(new_card)
                else:
                    break
            
            # Dealer hits or stands
            while dealer_hand.get_value() < 17:
                dealer_hand.add_card(deck.deal_card())
            
            # Conditions
            if player_hand.get_value() > 21:
                player.lose()
                row[1] = 1
            elif (player_hand.get_value() == 21) and ((player_hand.cards[0].value == "A") and (player_hand.cards[1].value in ['10','K','Q','J'])) or ((player_hand.cards[0].value in ['10','K','Q','J']) and (player_hand.cards[1].value == "A")):
                player.blackjack()
                row[0] += 1
                row[13] += 1
            elif dealer_hand.get_value() > 21:
                player.win()
                row[0] = 1
            elif player_hand.get_value() > dealer_hand.get_value():
                player.win()
                row[0] = 1
            elif player_hand.get_value() == dealer_hand.get_value():
                player.draw()
                row[2] = 1
            else:
                player.lose()
                row[1] = 1
            
            # Player's Cards
            row[10] = str(player_hand.cards[0])
            row[11] = str(player_hand.cards[1])
            # Dealer's Upcard
            row[12] = str(dealer_hand.cards[0])
            
            # Play Count
            row[4] = i + 1
            # Running Count
            row[3] = counter.get_running_count()
            # Player Hand
            row[5] = player_hand.get_value()
            # Dealer Hand
            row[6] = dealer_hand.get_value()
            # Balance
            row[7] = player.get_bankroll()
            
            # Append row to dataframe
            df.loc[len(df)] = row

            i += 1
    
    return df

def blackjack_lineplot(num_plays, starting_bankroll, base_bet, repetitions, strategy):
    
    # Plotting configurations
    fig, ax = plt.subplots()
    styling_configurations(fig, ax)

    # Setting size 
    fig.set_size_inches(10,4)

    # Labels
    ax.set_title(f"Number of Plays vs. ΔBalance, n = {repetitions}", color = 'white')
    ax.set_xlabel("Number of Plays", color = 'white')
    ax.set_ylabel("ΔBalance ($USD)", color = 'white')
    
    styling_configurations(fig, ax)
    for label in ax.get_xticklabels():
        label.set_color('white')
    for label in ax.get_yticklabels():
        label.set_color(color = 'white')

    # Create a DataFrame to hold the balances across all repetitions
    overall_df = pd.DataFrame(columns=['Play Count', 'Balance', 'Win', 'Loss', 'Draw'])

    for _ in range(repetitions):
        df = blackjack_simulator(num_plays, starting_bankroll, base_bet, strategy)
        ax.plot(df['Play Count'], df['Balance'], alpha=0.5)
        overall_df = pd.concat([overall_df, df[['Play Count', 'Balance', 'Win', 'Loss', 'Draw']]])

    # Calculate the mean of the balances at each play count
    mean_df = overall_df.groupby('Play Count', as_index=False).mean()
    
    # Perform linear regression on the overall data
    x = mean_df['Play Count'].astype(float)
    y = mean_df['Balance'].astype(float)
    slope, intercept = np.polyfit(x, y, 1)

    # Create x values for the line
    x_values = np.linspace(min(x), max(x), num_plays)

    # Compute corresponding y values
    y_values = slope * x_values + intercept

    # Plot the regression line
    ax.plot(x_values, y_values, color='white', linestyle='--')

    return fig, overall_df, slope


def blackjack_barchart(df, num_plays, repetitions):
    
    wins_avg = df['Win'].sum() / repetitions
    losses_avg = df['Loss'].sum() / repetitions
    draws_avg = df['Draw'].sum() / repetitions

    categories = ['Wins', 'Losses', 'Draws']
    values = [wins_avg, losses_avg, draws_avg]

    # Plotting configurations
    fig, ax = plt.subplots()
    styling_configurations(fig, ax)

    # Setting size 
    fig.set_size_inches(10,4)

    # Setting general colors and title
    ax.bar(categories, values, color='white', edgecolor='black')

    bars = ax.bar(categories, values, color='white', edgecolor='black')

    # Labels
    ax.set_title(f"Average results with {num_plays} plays, n = {repetitions}", color = 'white')
    ax.set_ylabel("Frequency", color = 'white')
    for label in ax.get_xticklabels():
        label.set_color('white')
    for label in ax.get_yticklabels():
        label.set_color(color = 'white')

    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, round(value, 2), 
                ha='center', va='bottom', color='red')

    return fig


def blackjack_distribution(df, num_plays, repeats):
    data = df[df.get('Play Count') == num_plays]
    
    # Plotting configurations
    fig, ax = plt.subplots()
    styling_configurations(fig, ax)

    # Setting size 
    fig.set_size_inches(10,4)

    # Setting general colors and title
    ax.hist(data['Balance'], bins=50, color='white', edgecolor='black')

    # Labels
    ax.set_title(f"Distribution of Ending Balances, n = {repeats}", color = 'white')
    ax.set_xlabel("Ending Balance ($USD)", color = 'white')
    ax.set_ylabel("Frequency", color = 'white')
    for label in ax.get_xticklabels():
        label.set_color('white')
    for label in ax.get_yticklabels():
        label.set_color(color = 'white')

    average_balance = data.get('Balance').mean()

    ax.axvline(x=average_balance, color='red', linestyle='--')

    # Displaying the average balance on the top left
    ax.text(0.05, 0.95, f'Average Balance: ${average_balance:.2f}', transform=ax.transAxes, 
            color='red', verticalalignment='top')

    return fig


def regressor(df):
    
    X = df[['Play Count']].values
    y = df['Balance']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Assign weights as inverse of variance
    weights = 1 / (y_train.var())

    model = LinearRegression() 
    model.fit(X_train, y_train, sample_weight=weights)

    # Predict each x value
    y_pred = model.predict(X_test)

    return model