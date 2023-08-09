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