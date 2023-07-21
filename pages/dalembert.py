import streamlit as st
from st_pages import add_page_title
import random
from packages.graphs import frequency_plot, line_plot, box_plot, stats_table, roulette_plot
from packages.data_manipulation import sample, dataframe_conversion

# Setting page configuration
st.set_page_config(
    page_title="D'Alembert",
    page_icon=":flower_playing_cards:",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

# Add page to list of pages
add_page_title()

# ----- BACKEND ----- #

# D'Alembert implementation
def dalembert(initial_balance, num_plays, base_bet, preference):
    """
    Simulates the D'Alembert strategy returning balance on roulette given an initial balance, number of plays, initial bet, and color preference  
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
    st.write("The *D'Alembert* roulette betting strategy weaves an intriguing dance of calculated progressions and the allure of a balanced recovery. Named after the renowned French mathematician Jean-Baptiste le Rond d'Alembert, this strategy employs a gradual approach to betting, incrementally increasing wagers after each loss and decreasing them after a win. Players navigate the twists and turns of chance, aiming to recoup losses while savoring the thrill of smaller wins. As the bet amounts sway with each spin, this strategy offers both structure and flexibility, enticing competitors to explore the captivating possibilities.")
    st.write("The algorithm for this strategy involves the following guidelines: ")
    st.text("1. Set an base bet")
    st.text("2. If you win a bet, subtract the bet by the base bet and continue.")
    st.text("3. If you lose a bet, add the base bet for the next round.")

# Handles form data
with col2:
    initial_balance = st.slider("Initial Balance", min_value=1, max_value=1000, value=200, step=1, help="Set the starting balance that you'll enter with")
    num_plays = st.slider("Number of Plays", min_value=10, max_value=500, value=10, step=1, help="Set the number of plays for the strategy")
    initial_bet = st.slider("Initial Bet", min_value=1, max_value=1000, value=10, step=1, help="Set the initial bet that you will build on")
    repeats = st.slider("Sample repetitions", min_value=10, max_value=1000, value=100, step=10, help="Set the **n** size for the number of samples")
    target_balance = st.slider("Target Balance", min_value=0, max_value=5000, value=0, step=10, help="Optional: Betting stops once the balance has reached or exceeds this value. Leave as 0 for no target.")
    preference = (st.selectbox("Color", options=['Red', 'Black', 'Green'])).lower()
    graph_width =  initial_bet * 20

# Subheader above the graphs
st.markdown(
    """
    <style>
    .custom-subheader {
        text-align: center; 
        font-family: Arial
    }
    </style>
    """,
    unsafe_allow_html=True,)
st.markdown('<h2 class="custom-subheader">Visualization</h2>', unsafe_allow_html=True)

# Simulate and convert into Pandas DataFrame
samples = sample(dalembert, repeats, initial_balance, num_plays, initial_bet, preference, target_balance if target_balance > 0 else None)
df = dataframe_conversion(samples)

# Initializes fig objects for our plots
line_plt = line_plot(dalembert, num_plays, initial_balance, initial_bet, preference)
frequency_plt = frequency_plot(df, initial_balance, repeats, graph_width)
box_plt = box_plot(df, initial_balance, repeats, graph_width)
stats_tbl = stats_table(df)

roulette_plot(line_plt, frequency_plt, box_plt, stats_tbl)
