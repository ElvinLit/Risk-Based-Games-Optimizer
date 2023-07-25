import streamlit as st
from st_pages import add_page_title
import random
from packages.graphs import frequency_plot, line_plot, box_plot, stats_table, roulette_plot
from packages.data_manipulation import sample, dataframe_conversion

# Setting page configuration
st.set_page_config(
    page_title="Martingale",
    page_icon=":blue_book:",
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Add page to list of pages
add_page_title()


# Martingale implementation
def martingale(initial_balance, num_plays, initial_bet, preference, target_balance, floor_balance = 0):
    """
    Simulates the martingale strategy returning balance on roulette given an initial balance, number of plays, initial bet, and color preference  
    Stops betting if balance reaches or exceeds target_balance.
    
    Args:
        initial_balance (int or float): Starting amount
        num_plays (int): Number of plays
        initial_bet (int or float): Starting amount
        preference (string): Color preference from "Red", "Black", or "Green"
        target_balance (int or float, optional): Target amount
    Returns:
        int or float: end amount
    """
    choices = ['red', 'black', 'green']
    weights = [18/38, 18/38, 2/38]
    balance = initial_balance
    bet = initial_bet
    ceiling = target_balance

    for _ in range(num_plays):
        if bet > balance or balance <= floor_balance or (ceiling is not None and balance >= ceiling):
            break
        outcome = random.choices(choices, weights)[0]
        if outcome == preference:
            balance += bet
            bet = initial_bet
        else:
            balance -= bet
            bet *= 2
    return balance


# Setting columns
col1, col2 = st.columns([1,1])

with col1:
    # Description of the strategy
    st.write("The **martingale system** is a betting strategy typically used \
             for Roulette. It is an algorithm with the goal of making back net losses as \
             quickly as possible, albeit containing much higher risk as well. The name 'Martingale' \
             is believed to have originated from a French gambling term 'Martingale,' which \
             referred to a style of strapping, or harness, that was used to fasten a horse's girth. \
             The betting system was given this name because it metaphorically represented the idea of \
             doubling down on bets after a loss, as if tightening the reins on a horse to keep it under control.")
    st.write("The strategy can be algorithmically described simply as follows: ")
    st.text("1. Set an initial bet")
    st.text("2. If you win a bet, reset the bet to the initial bet and continue.")
    st.text("3. If you lose a bet, double the bet for the next round.")
    st.text("4. Loop back into step 2.")

# Handles form data
with col2:
    initial_balance = st.slider("Initial Balance", min_value=1, max_value=1000, value=200, step=1, help="Set the starting balance that you'll enter with")
    num_plays = st.slider("Number of Plays", min_value=10, max_value=500, value=10, step=1, help="Set the number of plays for the strategy")
    initial_bet = st.slider("Initial Bet", min_value=1, max_value=1000, value=10, step=1, help="Set the initial bet that you will build on")
    repeats = st.slider("Sample repetitions", min_value=10, max_value=1000, value=100, step=10, help="Set the **n** size for the number of samples")
    target_balance = st.slider("Target Balance", min_value=0, max_value=5000, value=0, step=10, help="Optional: Betting stops once the balance has reached or exceeds this value. Leave as 0 for no target.")
    if target_balance > 0 and target_balance <= initial_balance:
        st.error("Target balance must be greater than initial balance.")
        st.stop()
    if target_balance == 0:
        target_balance = None
    floor_balance = st.slider("Floor Balance", min_value=0, max_value=1000, value=0, step=10, help="Optional: Betting stops once the balance has fallen under this value. Leave as 0 for no floor.")
    preference = (st.selectbox("Color", options=['Red', 'Black', 'Green'])).lower()
    graph_width =  initial_bet * 20

# Subheader above graph
st.markdown(
    """
    <style>
    .custom-subheader {
        text-align: center; 
        font-family: monospace
    }
    </style>
    """,
    unsafe_allow_html=True,)
st.markdown('<h2 class="custom-subheader">Visualizations</h2>', unsafe_allow_html=True)

# Simulate and convert into Pandas DataFrame
samples = sample(martingale, repeats, initial_balance, num_plays, initial_bet, preference, target_balance, floor_balance)
martingale_df = dataframe_conversion(samples)

# Initializes fig objects for our plots
line_plt = line_plot(martingale, num_plays, initial_balance, initial_bet, preference, target_balance)
frequency_plt = frequency_plot(martingale_df, initial_balance, repeats, graph_width)
box_plt = box_plot(martingale_df, initial_balance, repeats, graph_width)
stats_tbl = stats_table(martingale_df, initial_balance)

roulette_plot(line_plt, frequency_plt, box_plt, stats_tbl)