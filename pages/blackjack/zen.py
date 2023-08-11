import streamlit as st
from st_pages import add_page_title
import random
from packages.blackjack_logic import Deck, CardCounter, Hand, hit_or_stand
import pandas as pd

# Setting page configuration
st.set_page_config(
    page_title="Zen",
    page_icon=":flower_playing_card:",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

# Add page to list of pages
add_page_title()

col1, col2 = st.columns([1,1])

def blackjack_zen_simulator(num_plays):
    """
    Simulates a Blackjack game using the zen counting strategy. 
    Args:
        num_plays (int): number of plays for the simulation
    Returns:
        DataFrame: contains information with columns ['Win', 'Loss', 'Draw', 'Running Count', 'Play Count']
    """

    deck = Deck()
    counter = CardCounter()
    
    df = pd.DataFrame(columns=['Win', 'Loss', 'Draw', 'Running Count', 'Play Count', 'Player Hand Value', 'Dealer Hand Value'])

    for i in range(num_plays):

        # Initialize our row for the dataframe
        row = [None] * 7
        
        # New hands each round
        player_hand = Hand()
        dealer_hand = Hand()

        # Check for deck exhaustion 
        if len(deck.cards) < 10: # Arbitrary threshold
            deck = Deck() 
            counter.reset_count()

        # Initial Dealing, 2 cards each, assume only the dealer's first card is shown to the player
        for j in range(2):
            player_card = deck.deal_card()
            dealer_card = deck.deal_card()

            player_hand.add_card(player_card)
            dealer_hand.add_card(dealer_card)

            counter.zen(player_card)
            if j == 0:
                counter.zen(dealer_card)
        
        # Modify the count based on shown cards
        count = counter.get_running_count()
            
        # Hit or Stand
        while player_hand.get_value() < 21:
            action = hit_or_stand(player_hand, dealer_hand.cards[0], count)
            if action:
                new_card = deck.deal_card()
                player_hand.add_card(new_card)
                counter.zen(new_card)
            else:
                break
        
        # Dealer hits or stands
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
        
        # Conditions
        if dealer_hand.get_value() > 21:
            row[0] = 1
        elif player_hand.get_value() > dealer_hand.get_value():
            row[0] = 1
        elif player_hand.get_value() == dealer_hand.get_value():
            row[2] = 1
        else:
            row[1] = 1
        
        # Play Count
        row[4] = i + 1
        # Running Count
        row[3] = counter.get_running_count()
        # Player Hand
        row[5] = player_hand.get_value()
        # Dealer Hand
        row[6] = dealer_hand.get_value()

        # Append row to dataframe
        df.loc[len(df)] = row
    
    return df

st.write(blackjack_zen_simulator(100))