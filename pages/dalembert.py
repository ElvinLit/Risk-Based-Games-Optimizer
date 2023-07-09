import streamlit as st
from st_pages import Page, show_pages, add_page_title
import random
from packages.methods import sample, dataframe_conversion, frequency_plot

# Setting page configuration
st.set_page_config(
    page_title="D'Alembert",
    page_icon=":green_book:",
    layout="wide" 
)

# Add page to list of pages
add_page_title()

# D'Alembert implementation
def dalembert(initial_balance, num_plays, base_bet, preference):
    """
    Simulates the D'Alembert strategy returning balance on roulette given an initial balance, number of plays, initial bet, and color preference  

    Args:
        starting_balance (int or float): Starting amount
        num_plays (int): Number of plays
        initial_bet (int or float): Starting amount
        preference (string): Color preference from "Red", "Black", or "Green"
    Returns:
        int or float: end amount
    """
    choices = ['red', 'black', 'green']
    weights = [18/38, 18/38, 2/38]
    balance = initial_balance
    bet = base_bet
    
    for i in range(num_plays):
        if balance <= 0:
            break
        outcome = random.choices(choices, weights)[0]
        if outcome == preference:
            balance += bet
            bet -= base_bet
            if bet <= 0:
                bet = base_bet
        else:
            balance -= bet
            bet += base_bet
            if bet >= balance:
                bet = balance
    return balance


# ----- FRONTEND ----- #

# Description of the strategy
st.write("The **D'Alembert system** is a betting strategy used for Roulette. It is an algorithm with the goal of playing conservatively. The allure of this strategy surrounds the superficial ease of a balanced recovery after loss.")
st.write("The algorithm for this strategy involves the following guidelines: ")
st.text("1. Set an base bet")
st.text("2. If you win a bet, subtract the bet by the base bet and continue.")
st.text("3. If you lose a bet, add the base bet for the next round.")

# Handles form data
st.subheader("Visualize based on your parameters")

with st.form(key='martingale_parameters'):
    initial_balance = st.number_input("Initial Balance")
    num_plays = int(st.number_input("Number of Plays"))
    base_bet = st.number_input("Base Bet")
    preference = (st.text_input("Color (choose from 'Red', 'Black', or 'Green')")).lower()
    repeats =  int(st.number_input("Sample repetitions"))
    
    submit_button = st.form_submit_button(label='Visualize')

if submit_button:
    samples = sample(dalembert, repeats, initial_balance, num_plays, base_bet, preference)
    dalembert_df = dataframe_conversion(samples)
    frequency_plot(dalembert_df, initial_balance, repeats)