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

# Setting columns
col1, col2 = st.columns([1,1])

with col1:
    # Description of the strategy
    st.write("The **martingale system** is a betting strategy typically used for Roulette. It is an algorithm with the goal of making back net losses as quickly as possible, albeit containing much higher risk as well.")
    st.write("The strategy can be algorithmically described simply as follows: ")
    st.text("1. Set an initial bet")
    st.text("2. If you win a bet, reset the bet to the initial bet and continue.")
    st.text("3. If you lose a bet, double the bet for the next round.")

# Subheader 
st.markdown(
    """
    <style>
    .custom-subheader {
        text-align: center; 
        font-family: Helvetica
    }
    </style>
    """,
    unsafe_allow_html=True,)
st.markdown('<h2 class="custom-subheader">Visualizations</h2>', unsafe_allow_html=True)

# Handles form data
with col2:
    initial_balance = st.slider("Initial Balance", min_value=1, max_value=1000, value=200, step=1)
    num_plays = st.slider("Number of Plays", min_value=10, max_value=500, value=10, step=1)
    initial_bet = st.slider("Initial Bet", min_value=1, max_value=1000, value=10, step=1)
    repeats = st.slider("Sample repetitions", min_value=10, max_value=1000, value=100, step=10)
    target_balance = st.slider("Target Balance", min_value=0, max_value=5000, value=0, step=10, help="Optional: Betting stops once the balance has reached or exceeds this value. Leave as 0 for no target.")
    preference = (st.selectbox("Color", options=['Red', 'Black', 'Green'])).lower()
    graph_width =  initial_bet * 20

# Simulate and convert into Pandas DataFrame
samples = sample(martingale, repeats, initial_balance, num_plays, initial_bet, preference, target_balance if target_balance > 0 else None)
martingale_df = dataframe_conversion(samples)

# Initializes fig objects for our plots
line_plt = line_plot(martingale, num_plays, initial_balance, initial_bet, preference)
frequency_plt = frequency_plot(martingale_df, initial_balance, repeats, graph_width)
box_plt = box_plot(martingale_df, initial_balance, repeats, graph_width)

roulette_plot(line_plt, frequency_plt, box_plt)