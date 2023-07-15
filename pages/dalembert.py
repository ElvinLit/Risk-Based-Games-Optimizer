import streamlit as st
from st_pages import Page, show_pages, add_page_title
import random
from packages.graphs import frequency_plot, line_plot, box_plot, roulette_plot
from packages.data_manipulation import sample, dataframe_conversion

# Setting page configuration
st.set_page_config(
    page_title="D'Alembert",
    page_icon=":flower_playing_cards:",
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
        if balance <= bet:
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
# Setting columns
col1, col2 = st.columns([1,1])

with col1:
    # Description of the strategy
    st.write("The **D'Alembert system** is a betting strategy used for Roulette. It is an algorithm with the goal of playing conservatively. The allure of this strategy surrounds the superficial ease of a balanced recovery after loss.")
    st.write("The algorithm for this strategy involves the following guidelines: ")
    st.text("1. Set an base bet")
    st.text("2. If you win a bet, subtract the bet by the base bet and continue.")
    st.text("3. If you lose a bet, add the base bet for the next round.")


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


# Handles form data
with col2:
    initial_balance = st.slider("Initial Balance", min_value=1, max_value=1000, value=200, step=1)
    num_plays = st.slider("Number of Plays", min_value=10, max_value=500, value=10, step=1)
    initial_bet = st.slider("Initial Bet", min_value=1, max_value=1000, value=10, step=1)
    repeats = st.slider("Sample repetitions", min_value=10, max_value=1000, value=100, step=10)
    target_balance = st.slider("Target Balance", min_value=0, max_value=5000, value=0, step=10, help="Optional: Betting stops once the balance has reached or exceeds this value. Leave as 0 for no target.")
    preference = (st.selectbox("Color", options=['Red', 'Black', 'Green'])).lower()
    graph_width =  initial_bet * 20

samples = sample(dalembert, repeats, initial_balance, num_plays, initial_bet, preference, target_balance if target_balance > 0 else None)
martingale_df = dataframe_conversion(samples)
roulette_plot(line_plot(dalembert, num_plays, initial_balance, initial_bet, preference), frequency_plot(martingale_df, initial_balance, repeats, graph_width), box_plot(martingale_df, initial_balance, repeats, graph_width))