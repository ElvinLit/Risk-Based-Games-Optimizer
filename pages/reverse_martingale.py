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
def reverse_martingale(initial_balance, num_plays, initial_bet, preference):
    """
    Simulates the martingale strategy returning balance on roulette given an initial balance, number of plays, initial bet, and color preference  

    Args:
        starting_balance (int or float): Starting amount
        num_plays (int): Number of plays
        initial_bet (int or float): Starting amount
        preference (string): Color preference from "Red", "Black", or "Green"
    Returns:
        int or float: end amount
    """
    choices = ['Red', 'Black', 'Green']
    weights = [18/38, 18/38, 2/38]
    
    balance = initial_balance
    bet = initial_bet
    for _ in range(num_plays):
        outcome = random.choices(choices, weights)[0]
        if outcome == preference:
            balance += bet
            bet *= 2
        else:
            balance -= bet
            bet = initial_bet
    return balance


# ----- FRONTEND ----- #

# Description of the strategy
st.write("The **reverse martingale system** is the reverse of the Martingale strategy. \
         It is more attractive to traders than its counterpart due to the nature of the momentus markets, \
         but this strategy's origin was for betting applications. It is an algorithm with the goal of maximizing \
         profits on winning streaks and minimizing the losses on losing streaks.")
st.write("The strategy can be algorithmically described simply as follows: ")
st.text("1. Set an initial bet")
st.text("2. If you win a bet, reset the bet to the initial bet and continue.")
st.text("3. If you lose a bet, double the bet for the next round.")

# Handles form data
st.subheader("Visualize based on your parameters")

with st.form(key='reverse_martingale_parameters'):
    initial_balance = st.number_input("Initial Balance")
    num_plays = int(st.number_input("Number of Plays"))
    initial_bet = st.number_input("Initial Bet")
    preference = st.text_input("Color (choose from 'Red', 'Black', or 'Green')")
    repeats =  int(st.number_input("Sample repetitions"))
    
    submit_button = st.form_submit_button(label='Visualize')

if submit_button:
    samples = sample(reverse_martingale, repeats, initial_balance, num_plays, initial_bet, preference)
    martingale_df = dataframe_conversion(samples)
    frequency_plot(martingale_df, initial_balance)



