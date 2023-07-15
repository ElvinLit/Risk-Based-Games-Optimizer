import streamlit as st
from st_pages import Page, show_pages, add_page_title
import random
from packages.graphs import frequency_plot, line_plot, box_plot, roulette_plot
from packages.data_manipulation import sample, dataframe_conversion

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

    # Handles form data

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
st.markdown('<h2 class="custom-subheader">Visualize Based on your Parameters</h2>', unsafe_allow_html=True)

with col2:
    with st.form(key='dalembert_parameters'):
        # Argument entries
        initial_balance_text = st.text_input("Initial Balance", placeholder= '200')
        num_plays_text = st.text_input("Number of Plays", placeholder= '10')
        initial_bet_text = st.text_input("Initial Bet", placeholder= '10')
        preference = (st.selectbox("Color", options=['Red', 'Black', 'Green'])).lower()
        repeats_text =  st.text_input("Sample repetitions", placeholder= '100')
        target_balance_text = st.text_input("Target Balance", placeholder = "None", help="Optional: Betting stops once the balance has reached or exceeds this value. Leave None for no target.")

        # Submit button
        submit_button = st.form_submit_button(label='Visualize')

if submit_button:
    try:
        initial_balance = float(initial_balance_text)
        num_plays = int(num_plays_text)
        base_bet = float(initial_bet_text)
        repeats =  int(repeats_text)
        if target_balance_text.upper() == "" or "NONE":
            target_balance = 0.0
        else: 
            target_balance = float(target_balance_text)
        graph_width =  base_bet * 20 

    except ValueError:
        st.error("Please enter valid numeric inputs in the form fields.")

    samples = sample(dalembert, repeats, initial_balance, num_plays, base_bet, preference, target_balance if target_balance > 0 else None)
    dalembert_df = dataframe_conversion(samples)
    roulette_plot(line_plot(dalembert, num_plays, initial_balance, base_bet, preference), frequency_plot(dalembert_df, initial_balance, repeats, graph_width), box_plot(dalembert_df, initial_balance, repeats, graph_width))