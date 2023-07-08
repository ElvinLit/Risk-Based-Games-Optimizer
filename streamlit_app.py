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
