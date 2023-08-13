import streamlit as st
from st_pages import add_page_title
import random
from packages.blackjack_logic import Deck, CardCounter, Hand, Player, hit_or_stand, double_down
from packages.graphs import blackjack_histogram, styling_configurations
import pandas as pd
import matplotlib.pyplot as plt 

# Setting page configuration
st.set_page_config(
    page_title="High Low",
    page_icon=":flower_playing_card:",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

# Add page to list of pages
add_page_title()

col1, col2 = st.columns([1,1])

def blackjack_hl_simulator(num_plays, starting_bankroll, base_bet):
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
    
    df = pd.DataFrame(columns=['Win', 'Loss', 'Draw', 'Running Count', 'Play Count', 'Player Hand Value', 'Dealer Hand Value', 'Balance'])

    for i in range(num_plays):

        # Initialize our row for the dataframe
        row = [None] * 8
        
        # New hands each round
        player_hand = Hand()
        dealer_hand = Hand()

        # Check for deck exhaustion 
        if len(deck.cards) < 10: # Arbitrary threshold
            deck = Deck() 
            counter.reset_count()

        # Set bet size based on count (you can modify the logic here)
        bet_size = base_bet 
        player.place_bet(bet_size)

        # Initial Dealing, 2 cards each, assume only the dealer's first card is shown to the player
        for j in range(2):
            player_card = deck.deal_card()
            dealer_card = deck.deal_card()

            player_hand.add_card(player_card)
            dealer_hand.add_card(dealer_card)

            counter.high_low(player_card)
            if j == 0:
                counter.high_low(dealer_card)
        
        # Modify the count based on shown cards
        count = counter.get_running_count()
        
        # Double bet if applicable
        if double_down(player_hand, dealer_hand.cards[0], count) == True:
            player.place_bet(bet_size)
            bet_size += base_bet
            
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
        if player_hand.get_value() > 21:
            player.lose()
            row[1] = 1
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
    
    return df

df_info = blackjack_hl_simulator(1000, 1000, 50)

st.pyplot(blackjack_histogram(df_info, 1000))

def blackjack_lineplot(num_plays, starting_bankroll, base_bet, repetitions):
    
    # Plotting configurations
    fig, ax = plt.subplots()
    styling_configurations(fig, ax)

    # Setting size 
    fig.set_size_inches(10,4)

    # Labels
    ax.set_title("Scatterplot for Number of Plays vs. Ending Balance", color = 'white')
    ax.set_xlabel("Number of Plays", color = 'white')
    ax.set_ylabel("Ending Balances", color = 'white')
    
    styling_configurations(fig, ax)
    for label in ax.get_xticklabels():
        label.set_color('white')
    for label in ax.get_yticklabels():
        label.set_color(color = 'white')

    for _ in range(repetitions):
        df = blackjack_hl_simulator(num_plays, starting_bankroll, base_bet)
        ax.plot(df['Play Count'], df['Balance'])

    return fig


st.pyplot(blackjack_lineplot(1000, 1000, 50, 20))

st.dataframe(df_info)

st.write(df_info['Win'].sum())
st.write(df_info['Loss'].sum())
st.write(df_info['Draw'].sum())