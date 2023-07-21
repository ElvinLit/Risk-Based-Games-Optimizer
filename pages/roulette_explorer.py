import streamlit as st
from st_pages import add_page_title

# Setting page configuration
st.set_page_config(
    page_title="Roulette Strategy Explorer",
    page_icon=":orange_book:",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

# Add page to list of pages
add_page_title()

# ----- BACKEND ----- #

# ----- FRONTEND ----- #

col1, col2 = st.columns([1,1])
with col1:
    st.header('Overview of Roulette')
    st.write("*Roulette* is a popular casino game where players bet on a color, number, or various combinations of the two. For the purposes of our page, \
             we allow users to only select colors as they represent the highest chances of winning: **18/38** for Red or Black, **2/38** for Green.")
    st.write("As seen, even the best chance of winning is less than 50%. The Expected Value (EV) can be calculated statistically. Let P be \
            the probability of winning, Q=1-P be the probability of losing, and a bet of $10. Thus follows: ")
    st.latex(r'''
        \begin{align*}
            p &= \frac{18}{37} \approx 0.4865, \phantom{q} & q = 1 - p \approx 0.5135.
        \end{align*}
        ''')
    st.latex(r'''
        \begin{align*}
            \text{EV (win)} &= (p \times \text{Profit per win}) - (q \times \text{Loss per loss}) = (0.4865 \times 10) - (0.5135 \times 10) = -0.275.
        \end{align*}
        ''')
    st.latex(r'''
        \begin{align*}
            \text{EV (loss)} &= (q \times \text{Loss per loss}) - (p \times \text{Profit per win}) = (0.5135 \times 20) - (0.4865 \times 10) = -2.815.
        \end{align*}     
        ''')
    st.latex(r'''
    \begin{align*}
        \text{EV (one round)} &= (p \times \text{EV (win)}) + (q \times \text{EV (loss)}) \approx -1.580.
    \end{align*}
        ''')
    st.write("As you can see, given an initial bet of 10 dollars, we are expected to lose around 1.58 dollars on every round that we play. However, we have different betting \
             systems that you are free to play around with to try and find a 'winning' strategy. On this page, you can compare the graphs for these strategies based on your parameters.")
    
with col2:
    initial_balance = st.slider("Initial Balance", min_value=1, max_value=1000, value=200, step=1, help="Set the starting balance that you'll enter with")
    num_plays = st.slider("Number of Plays", min_value=10, max_value=500, value=10, step=1, help="Set the number of plays for the strategy")
    initial_bet = st.slider("Initial Bet", min_value=1, max_value=1000, value=10, step=1, help="Set the initial bet that you will build on")
    repeats = st.slider("Sample repetitions", min_value=10, max_value=1000, value=100, step=10, help="Set the **n** size for the number of samples")
    target_balance = st.slider("Target Balance", min_value=0, max_value=5000, value=0, step=10, help="Optional: Betting stops once the balance has reached or exceeds this value. Leave as 0 for no target.")
    if target_balance > 0 and target_balance <= initial_balance:
        target_balance = None
    floor_balance = st.slider("Floor Balance", min_value=0, max_value=5000, value=0, step=10, help="Optional: Betting stops once the balance has fallen under this value. Leave as 0 for no floor.")
    preference = (st.selectbox("Color", options=['Red', 'Black', 'Green'])).lower()
    graph_width =  initial_bet * 20

    