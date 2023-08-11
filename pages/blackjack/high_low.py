import streamlit as st
from st_pages import add_page_title
import random
from packages.blackjack_logic import Deck, CardCounter, Hand, hit_or_stand

# Setting page configuration
st.set_page_config(
    page_title="High Low",
    page_icon=":flower_playing_card:",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

# Add page to list of pages
add_page_title()

def blackjack_hl_simulator(num_plays):
    """
    Simulates a Blackjack game using the zen counting strategy. 
    Args:
        num_plays (int): number of plays for the simulation
    Returns:
        tuple: (number of wins, number of draws, number of losses, number of plays)
    """

    deck = Deck()
    counter = CardCounter()

    num_wins = 0
    num_draws = 0
    num_losses = 0
    
    for _ in range(num_plays):
        
        # New hands each round
        player_hand = Hand()
        dealer_hand = Hand()

        # Check for deck exhaustion 
        if len(deck.cards) < 10: # Arbitrary threshold
            deck = Deck() 
            counter.reset_count()

        #Initial Dealing, 2 cards each, assume only the dealer's first card is shown to the player
        for i in range(2):
            player_card = deck.deal_card()
            dealer_card = deck.deal_card()

            player_hand.add_card(player_card)
            dealer_hand.add_card(dealer_card)

            counter.high_low(player_card)
            if i == 0:
                counter.high_low(dealer_card)
        
        #Modify the count based on shown cards
        count = counter.get_running_count()
            
        # Hit or Stand
        while player_hand.get_value() < 21:
            action = hit_or_stand(player_hand, dealer_hand.cards[0], count)
            if action:
                new_card = deck.deal_card()
                player_hand.add_card(new_card)
                counter.high_low(new_card)
            else:
                break
        
        # Dealer hits or stands
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
        
        # Conditions
        if dealer_hand.get_value() > 21:
            num_wins += 1
        elif player_hand.get_value() > dealer_hand.get_value():
            num_wins += 1
        elif player_hand.get_value() == dealer_hand.get_value():
            num_draws += 1 
        else:
            num_losses +=1 
    
    return num_wins, num_draws, num_losses, num_plays

st.write(blackjack_hl_simulator(100))