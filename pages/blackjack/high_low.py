import streamlit as st
from st_pages import add_page_title

from packages.blackjack_logic import blackjack_hl_simulator, blackjack_lineplot, blackjack_barchart, blackjack_distribution, random_forest_regressor

import random
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np




# Setting page configuration
st.set_page_config(
    page_title="High Low",
    page_icon=":flower_playing_card:",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

# Add page to list of pages
add_page_title()

col1, col2 = st.columns([1,1])

st.divider()

with col1:
    # Strategy description
    st.write("In Blackjack, there are various counting strategies aimed to minimize the house edge over the player. \
             First discovered by American mathematician and hedge fund manager Edward Thorp in the 1960s, the hi-lo \
             counting strategy assigns a count of -1 to Aces, face cards, and 10s, a count of 0 to 9s, 8s, and 7s, \
             and a count of +1 to 6s, 5s, 4s, 3s, and 2s. Upon the dealer shuffling the deck, the player will keep \
             a mental count once cards are dealt, and use that count to adjust their strategies. Based on pre-defined \
             rules that cover every possible Blackjack hand, the player will act accordingly. By implementing these \
             findings into Python code and simulations, one can see how the ending results produce an overall positive \
             result. The simulations are designed to imitate perfect counting with hi-lo, and the player's actions \
             reflect that of 'basic strategy' and the illustrious 18, which define deviations from basic strategy \
             depending on the count.")
with col2:
    with st.form(key='parameters'):
        with st.container():
            num_plays = st.slider("Number of Plays", min_value=10, max_value=500, value=200, step=1, help="Set the number of plays for the strategy")
            starting_balance = st.slider('Starting Balance', min_value=10, max_value=1000, value=0, step=10, help="Set the starting balance")
            initial_bet = st.slider("Initial Bet", min_value=1, max_value=1000, value=10, step=1, help="Set the initial bet that you will build on")
            repeats = st.slider("Sample repetitions", min_value=10, max_value=1000, value=100, step=10, help="Set the **n** size for the number of samples")
        st.form_submit_button(label="Generate")
    
df_info_mc = blackjack_lineplot(num_plays, starting_balance, initial_bet, repeats, blackjack_hl_simulator)

st.pyplot(df_info_mc[0])

st.divider()

col3, col4 = st.columns([1,1])
with col3:
    st.pyplot(blackjack_distribution(df_info_mc[1], num_plays, repeats))
with col4:
    st.pyplot(blackjack_barchart(df_info_mc[1], num_plays, repeats))

st.divider()

st.subheader('Experimental Value')
st.write("Through Monte Carlo simulations, we are able to roughly estimate the expected value of each \
         play given our parameters. To do so, we first utilize a regression model to fit our numerous simulations \
         and capture the relationship between the play count and balance. As evident by the graph, the variance \
         increases as the play count increases. This effect is known as heteroscedasticity, and thus we cannot \
         use a purely linear model to fit our data. As such, I chose a random forest regressor for this \
         scenario, which combines the results of multiple decision trees into one result, thereby mimicking \
         the behavior of our simulations. After training this regressor, the user may input a play count to return \
         an expected value at that play count.")

col5, col6 = st.columns([1,1])
with col5:
    with st.form(key='predictor'):
        with st.container():
            predictor_count = st.slider("Insert play count: ", min_value=0, max_value=1000)
        
        predictor_button = st.form_submit_button(label="Predict")

    if predictor_button:
        st.write(f"Your experimental returns at {predictor_count} plays is ${round(random_forest_regressor(df_info_mc[1])[0].predict([[predictor_count]])[0], 2)}")