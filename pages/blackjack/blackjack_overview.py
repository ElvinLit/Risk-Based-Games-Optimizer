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

st.write("The blackjack simulator serves to mimic a 'perfect' strategy in playing Blackjack. \
         The game assumes a 6 deck shoe, dealer stands on all 17s, player can double after \
         splitting, can split up to 4 times, and can surrender. This is one of the most common \
         rulesets in Vegas.")