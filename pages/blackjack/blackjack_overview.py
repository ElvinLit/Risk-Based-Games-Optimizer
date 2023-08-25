import streamlit as st
from st_pages import add_page_title
import random

# Setting page configuration
st.set_page_config(
    page_title="About",
    page_icon="❔",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

# Add page to list of pages
add_page_title()

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
st.markdown('<h2 class="custom-subheader">Blackjack Overview</h2>', unsafe_allow_html=True)

st.write("Our web app runs Monte Carlo simulations on popular blackjack strategies: High-Low, Halves, and Zen. \
         Using basic strategy and deviation charts, we simulate game scenarios to see how each strategy might play out over time. \
         You'll get clear, easy-to-understand stats on ending balances from these simulations. Plus, if you're curious about how a \
         certain strategy might perform over a specific number of plays, our built-in regression model can give you a prediction. \
         Whether you're a seasoned player or just curious about blackjack, our tool offers insights to help you understand the game better.")