import streamlit as st
from st_pages import add_page_title
import random
from packages.blackjack_logic import Deck, CardCounter, Hand, Player, hit_or_stand, double_down, should_split, split_hands
from packages.graphs import blackjack_histogram, styling_configurations
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np

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

            counter.high_low(player_card)
            if j == 0:
                counter.high_low(dealer_card)
        
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
                        counter.high_low(new_card)
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
                counter.high_low(double_new_card)
            
            # Hit or Stand
            while (player_hand.get_value() < 21) and (double_bool == False):
                action = hit_or_stand(player_hand, dealer_hand.cards[0], counter.get_running_count())
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


df_info = blackjack_hl_simulator(1000, 0, 10)

# st.pyplot(blackjack_histogram(df_info, 10))

def blackjack_lineplot(num_plays, starting_bankroll, base_bet, repetitions):
    
    # Plotting configurations
    fig, ax = plt.subplots()
    styling_configurations(fig, ax)

    # Setting size 
    fig.set_size_inches(10,4)

    # Labels
    ax.set_title(u"Line Plot for Number of Plays vs. Δ Balance", color = 'white')
    ax.set_xlabel("Number of Plays", color = 'white')
    ax.set_ylabel("Δ Balance ($USD)", color = 'white')
    
    styling_configurations(fig, ax)
    for label in ax.get_xticklabels():
        label.set_color('white')
    for label in ax.get_yticklabels():
        label.set_color(color = 'white')

    # Create a DataFrame to hold the balances across all repetitions
    overall_df = pd.DataFrame(columns=['Play Count', 'Balance'])

    for i in range(repetitions):
        df = blackjack_hl_simulator(num_plays, starting_bankroll, base_bet)
        ax.plot(df['Play Count'], df['Balance'], alpha=0.5)
        overall_df = pd.concat([overall_df, df[['Play Count', 'Balance']]])

    # Calculate the mean of the balances at each play count
    overall_df = overall_df.groupby('Play Count', as_index=False).mean()
    
    # Perform linear regression on the overall data
    x = overall_df['Play Count'].astype(float)
    y = overall_df['Balance'].astype(float)
    slope, intercept = np.polyfit(x, y, 1)

    # Create x values for the line
    x_values = np.linspace(min(x), max(x), 100)

    # Compute corresponding y values
    y_values = slope * x_values + intercept

    # Plot the regression line
    ax.plot(x_values, y_values, color='white', linestyle='--')

    return fig




st.pyplot(blackjack_lineplot(1000, 0, 10, 25))

st.dataframe(df_info)

st.write(df_info['Win'].sum())
st.write(df_info['Loss'].sum())
st.write(df_info['Draw'].sum())
st.write(df_info.get('Balance').mean())