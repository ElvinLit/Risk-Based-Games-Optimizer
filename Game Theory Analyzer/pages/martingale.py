import streamlit as st
from st_pages import Page, show_pages, add_page_title

# Add page to list of pages
add_page_title()

st.write("The **martingale system** is a betting strategy typically used for Roulette. It is an algorithm with the goal of making back net losses as quickly as possible, albeit containing much higher risk as well.")
st.write("The strategy can be algorithmically described simply as follows: ")
st.text("1. Set an initial bet")
st.text("2. If you win a bet, reset the bet to the initial bet and continue.")
st.text("3. If you lose a bet, double the bet for the next round.")

coded_display = '''def Hello():
    print("Hello World!")'''
st.code(coded_display, language = 'python')

