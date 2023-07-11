import streamlit as st
from st_pages import Page, show_pages, add_page_title
import random
from packages.methods import sample, dataframe_conversion, frequency_plot

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
    initial_balance = st.number_input("Initial Balance")
    num_plays = int(st.number_input("Number of Plays"))
    initial_bet = st.number_input("Initial Bet")
    preference = (st.text_input("Color (choose from 'Red', 'Black', or 'Green')")).lower()
    repeats =  int(st.number_input("Sample repetitions"))
    target_balance = st.number_input("Target Balance", min_value=0.0, value=None, step=0.1, help="Optional: Betting stops once the balance has reached or exceeds this value. Leave blank for no target.") # new target_balance field
    # TESTING

    submit_button = st.form_submit_button(label='Visualize')

if submit_button:
    samples = sample(reverse_martingale, repeats, initial_balance, num_plays, initial_bet, preference, target_balance if target_balance > 0 else None)
    martingale_df = dataframe_conversion(samples)
    frequency_plot(martingale_df, initial_balance)
