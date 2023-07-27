import streamlit as st
from st_pages import Page, Section, show_pages, add_page_title

# Add page to our list of pages
add_page_title()

# Create sidebar with list of pages
show_pages(
    [
        Page("app.py", "Game Theory Analyzer", "🏠"),
        Section(name = "Roulette Betting Strategies"),
        Page("pages/roulette/roulette_overview.py", "About", '❔'),
        Page("pages/roulette/martingale.py", "Martingale System", "📖"),
        Page("pages/roulette/reverse_martingale.py", "Reverse Martingale System", "📖"),
        Page("pages/roulette/dalembert.py", "D'Alembert System", "📖"),
        Section(name = "Blackjack Counting Strategies"),
        Page("pages/blackjack/blackjack_overview.py", "About", '❔'),
        Page("pages/blackjack/high_low.py", "High Low", ":flower_playing_cards:"),
        Page("pages/blackjack/zen.py", "Zen", ":flower_playing_cards:"),
        Page("pages/blackjack/halves.py", "Halves", ":flower_playing_cards:")
    ]
)
