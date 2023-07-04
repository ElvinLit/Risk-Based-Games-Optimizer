import streamlit as st
from st_pages import Page, Section, show_pages, add_page_title

# Add page to our list of pages
add_page_title()

# Create sidebar with list of pages
show_pages(
    [
        Page("streamlit_app.py", "Game Theory Analyzer", "🏠"),
        Section(name = "Betting Strategies"),
        Page("pages/martingale.py", "Martingale System", "📖"),
        Page("pages/reverse_martingale.py", "Reverse Martingale System", "📖"),
        Page("pages/dalembert.py", "D'Alembert System", "📖")
    ]
)

# Creates textbox and button
# 19-20 Used to instantiate st.session_state
if "my_input" not in st.session_state: 
    st.session_state["my_input"] = ""

my_input = st.text_input("Input a text here", st.session_state["my_input"])
submit = st.button("Submit")
if submit:
    st.session_state["my_input"] = my_input
    st.write("You have entered: ", my_input)

