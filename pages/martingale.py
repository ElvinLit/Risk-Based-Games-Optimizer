import streamlit as st
from st_pages import add_page_title
import random
from packages.graphs import frequency_plot, line_plot, box_plot, roulette_plot
from packages.data_manipulation import sample, dataframe_conversion

# Setting configuration for our page
st.set_page_config(
    page_title="Martingale",
    page_icon=":blue_book:",
    layout="wide" 
)

# Add page to list of pages
add_page_title()

# ----- BACKEND ----- #

# Martingale implementation
def martingale(initial_balance, num_plays, initial_bet, preference):
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
    choices = ['red', 'black', 'green']
    weights = [18/38, 18/38, 2/38]
    
    balance = initial_balance
    bet = initial_bet

    for _ in range(num_plays):
        if balance <= bet:
            break
        outcome = random.choices(choices, weights)[0]
        if outcome == preference:
            balance += bet
            bet = initial_bet
        else:
            balance -= bet
            bet *= 2
    return balance


# ----- FRONTEND ----- #

# Description of the strategy
st.write("The **martingale system** is a betting strategy typically used for Roulette. It is an algorithm with the goal of making back net losses as quickly as possible, albeit containing much higher risk as well.")
st.write("The strategy can be algorithmically described simply as follows: ")
st.text("1. Set an initial bet")
st.text("2. If you win a bet, reset the bet to the initial bet and continue.")
st.text("3. If you lose a bet, double the bet for the next round.")

# Handles form data
st.subheader("Visualize based on your parameters")

with st.form(key='martingale_parameters'):
    initial_balance_text = st.text_input("Initial Balance", placeholder= '200')
    num_plays_text = st.text_input("Number of Plays", placeholder= '10')
    initial_bet_text = st.text_input("Initial Bet", placeholder= '10')
    preference = (st.selectbox("Color", options=['Red', 'Black', 'Green'])).lower()
    repeats_text =  st.text_input("Sample repetitions", placeholder= '100')
    target_balance_text = st.text_input("Target Balance", placeholder= 'None', help="Optional: Betting stops once the balance has reached or exceeds this value. Leave blank for no target.")
    submit_button = st.form_submit_button(label='Visualize')

if submit_button:
    
    # Verify the inputs are valid
    try:
        initial_balance = float(initial_balance_text)
        num_plays = int(num_plays_text)
        initial_bet = float(initial_bet_text)
        repeats =  int(repeats_text)
        if target_balance_text.upper() == "" or "NONE":
            target_balance = 0.0
        else: 
            target_balance = float(target_balance_text)
        graph_width =  initial_bet * 20

    except ValueError:
        st.error("Please enter valid numeric inputs in the form fields.")

    # Sample and plot
    samples = sample(martingale, repeats, initial_balance, num_plays, initial_bet, preference, target_balance if target_balance > 0 else None)
    martingale_df = dataframe_conversion(samples)
    roulette_plot(line_plot(martingale, num_plays, initial_balance, initial_bet, preference), frequency_plot(martingale_df, initial_balance, repeats, graph_width), box_plot(martingale_df, initial_balance, repeats, graph_width))