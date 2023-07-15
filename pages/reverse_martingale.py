import streamlit as st
from st_pages import Page, show_pages, add_page_title
import random
from packages.graphs import frequency_plot, line_plot, roulette_plot
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

# Handles form data
st.subheader("Visualize based on your parameters")

with st.form(key='reverse_martingale_parameters'):
    initial_balance_text = st.text_input("Initial Balance", placeholder= '200')
    num_plays_text = st.text_input("Number of Plays", placeholder= '10')
    initial_bet_text = st.text_input("Initial Bet", placeholder= '10')
    preference = (st.selectbox("Color", options=['Red', 'Black', 'Green'])).lower()
    repeats_text =  st.text_input("Sample repetitions", placeholder= '100')
    target_balance_text = st.text_input("Target Balance", placeholder= 'None', help="Optional: Betting stops once the balance has reached or exceeds this value. Leave None for no target.")
    submit_button = st.form_submit_button(label='Visualize')

if submit_button:
    try:
        initial_balance = float(initial_balance_text if initial_balance_text else '200')
        num_plays = int(num_plays_text if num_plays_text else '10')
        initial_bet = float(initial_bet_text if initial_bet_text else '10')
        repeats =  int(repeats_text if repeats_text else '100')
        
        if target_balance_text.upper() == "" or target_balance_text.upper() == "NONE":
            target_balance = 0.0
        else: 
            target_balance = float(target_balance_text)
        graph_width =  initial_bet * 20

    except ValueError:
        st.error("Please enter valid numeric inputs in the form fields.")

    samples = sample(reverse_martingale, repeats, initial_balance, num_plays, initial_bet, preference, target_balance if target_balance > 0 else None)
    reverse_martingale_df = dataframe_conversion(samples)
    roulette_plot(line_plot(reverse_martingale, num_plays, initial_balance, initial_bet, preference), frequency_plot(reverse_martingale_df, initial_balance, repeats, graph_width))