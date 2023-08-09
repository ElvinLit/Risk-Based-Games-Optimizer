import streamlit as st
from st_pages import Page, Section, show_pages, add_page_title

# Add page to our list of pages
add_page_title()

# Create sidebar with list of pages
show_pages(
    [
        Page("app.py", "Game Data Analytics", ":game_die:"),
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

# Adding Graphics and Text to home page
col1, col2 = st.columns([1, 1])
#with col1:
st.write("This web application was designed to analyze strategies for risk-based games, specifically focusing on roulette and blackjack. Statistical data for these games, as processed by our algorithms, are presented on the subsequent pages.")
image_url = "https://www.degonline.org/wp-content/uploads/2022/11/data-stock-photo.jpg" 
st.image(image_url, use_column_width=True)