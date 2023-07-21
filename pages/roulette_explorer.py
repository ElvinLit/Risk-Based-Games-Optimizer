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
st.markdown('<h2 class="custom-subheader">Roulette Overview</h2>', unsafe_allow_html=True)

st.write("*Roulette* is a popular casino game where players bet on a color, number, or various combinations of the two. For the purposes of our page, \
        we allow users to only select colors as they represent the highest chances of winning: **18/38** for Red or Black, **2/38** for Green. On a winning \
        bet, players win twice their bet amount, essentially net gaining the amount that they bet. From observing the possibilities, \
        it is evident that even the best chance of winning is less than 50%. The Expected Value (EV) can be calculated statistically. Let P be \
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
        systems that you are free to play around with to try and find a 'winning' strategy. Keep in mind that not every strategy is foolproof, and especially for roulette, \
        it is almost nearly impossible to find a completely winning strategy. These visualizations are meant to serve as fun observations, not guidelines for your \
        gambling endeavors.")