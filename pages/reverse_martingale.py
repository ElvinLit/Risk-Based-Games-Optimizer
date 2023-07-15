import streamlit as st
from st_pages import Page, show_pages, add_page_title
import random
from packages.graphs import frequency_plot, line_plot, box_plot, roulette_plot
from packages.data_manipulation import sample, dataframe_conversion

#test

# Setting configuration for our page
st.set_page_config(
    page_title="Reverse Martingale",
    page_icon=":orange_book:",
    layout="wide" 
)

# Add page to list of pages
add_page_title()

# ----- BACKEND ----- #

# Reverse Martingale implementation
def reverse_martingale(initial_balance, num_plays, initial_bet, preference, target_balance=None):
    """
    Simulates the martingale strategy returning balance on roulette given an initial balance, number of plays, initial bet, and color preference  
    Stops betting if balance reaches or exceeds target_balance.

    Args:
        initial_balance (int or float): Starting amount
        num_plays (int): Number of plays
        initial_bet (int or float): Starting amount
        preference (string): Color preference from "red", "black", or "green"
        target_balance (int or float, optional): Target amount
    Returns:
        int or float: end amount
    """
    choices = ['red', 'black', 'green']
    weights = [18/38, 18/38, 2/38]
    
    balance = initial_balance
    bet = initial_bet
    for _ in range(num_plays):
        if balance <= bet or (target_balance is not None and balance >= target_balance):
            break
        outcome = random.choices(choices, weights)[0]
        if outcome == preference:
            balance += bet
            bet *= 2
        else:
            balance -= bet
            bet = initial_bet
    return balance


# ----- FRONTEND ----- #
# Setting columns
col1, col2 = st.columns([1,1])

with col1:
    # Description of the strategy
    st.write("The **reverse martingale system** is the reverse of the Martingale strategy. \
            For traders, this strategy is better than its counterpart due to the momentous nature of markets, \
            but this strategy's origin was for betting applications. It is an algorithm with the goal of maximizing \
            profits on winning streaks and minimizing the losses on losing streaks.")
    st.write("The strategy can be algorithmically described simply as follows: ")
    st.text("1. Set an initial bet")
    st.text("2. If you win a bet, double the bet for the next round.")
    st.text("3. If you lose a bet, reset the bet to the initial bet and continue.")


# Subheader 
st.markdown(
    """
    <style>
    .custom-subheader {
        text-align: center; /* Change the text alignment to left */
        font-family: Arial
    }
    </style>
    """,
    unsafe_allow_html=True,)
st.markdown('<h2 class="custom-subheader">Visualization</h2>', unsafe_allow_html=True)

with col2:
    initial_balance = st.slider("Initial Balance", min_value=1, max_value=1000, value=200, step=1)
    num_plays = st.slider("Number of Plays", min_value=10, max_value=500, value=10, step=1)
    initial_bet = st.slider("Initial Bet", min_value=1, max_value=1000, value=1, step=1)
    repeats = st.slider("Sample repetitions", min_value=10, max_value=1000, value=100, step=10)
    target_balance = st.slider("Target Balance", min_value=0, max_value=5000, value=0, step=10, help="Optional: Betting stops once the balance has reached or exceeds this value. Leave as 0 for no target.")
    preference = (st.selectbox("Color", options=['Red', 'Black', 'Green'])).lower()

    graph_width =  initial_bet * 20

samples = sample(reverse_martingale, repeats, initial_balance, num_plays, initial_bet, preference, target_balance if target_balance > 0 else None)
reverse_martingale_df = dataframe_conversion(samples)
roulette_plot(line_plot(reverse_martingale, num_plays, initial_balance, initial_bet, preference), frequency_plot(reverse_martingale_df, initial_balance, repeats, graph_width), box_plot(reverse_martingale_df, initial_balance, repeats, graph_width))