import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from packages.data_manipulation import sample, dataframe_conversion

def frequency_plot(df, initial_balance, repeats, graph_width):
    """
    Creates a matplotlib plot that visualizes the returns based on user input
    Args:
        df (DataFrame): dataframe that we are plotting
        initial_balance (int or float): the initial balance based on user input
    Returns:
        None
    """
    
    # Plotting configurations
    
    fig, ax = plt.subplots()
    fig.set_facecolor('#0E1117')

    plt.rcParams['font.family'] = 'Serif'

    # Setting range for our graph
    lower_range = df['Balance'].mean() - graph_width
    upper_range = df['Balance'].mean() + graph_width

    # Setting general colors and title
    ax.hist(df['Balance'], bins=50, range=(lower_range, upper_range), color='white', edgecolor='black')
    ax.set_facecolor('#0E1117')

    # Setting axes position 
    ax.spines['top'].set_position(('outward', 0))
    ax.spines['bottom'].set_position(('outward', 0))
    ax.spines['left'].set_position(('outward', 0))
    ax.spines['right'].set_position(('outward', 0))

    # Setting border colors
    ax.spines['top'].set_color('white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')

    # Setting axes text color
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='y', color='white')
    ax.tick_params(axis='x', color='white')
    
    # Labels
    ax.set_title("Frequency Histogram of different Returns, n = " + str(repeats), color = 'white')
    ax.set_xlabel("Ending Balance", color = 'white')
    ax.set_ylabel("Frequency", color = 'white')
    ax.axvline(x=initial_balance, color='red', linestyle='--')
    for label in ax.get_xticklabels():
        label.set_color('white')
    for label in ax.get_yticklabels():
        label.set_color(color = 'white')

    # Setting fonts
    

    # Calculating annotation location
    hist, bin_edges = np.histogram(df['Balance'], bins=50, range=(lower_range, upper_range))
    filtered_hist = hist[(bin_edges[:-1] >= lower_range) & (bin_edges[1:] <= upper_range)]

    ax.annotate(f'STARTING BALANCE: {initial_balance}', xy=(initial_balance, 0), xytext=(initial_balance, np.mean(filtered_hist)),
             arrowprops=dict(arrowstyle='->', color = "Red"), color = "Red")
    
    # Setting size 
    fig.set_size_inches(10,4)
    '''
        col1, col2 = st.columns([1, 1])
        with col1:
    '''
    st.pyplot(fig, use_container_width=True)

def line_plot(strategy, num_plays, initial_balance, initial_bet, preference):
    """
    Creates a matplotlib line plot that visualizes the returns vs number of plays
    Args:
       Args:
        df (DataFrame): dataframe that we are plotting
        num_plays (int): number of plays
        initial_balance (int or float): the initial balance based on user input
        initial_bet (int or float): starting amount
        preference (string): Color preference from "red", "black", or "green"

    Returns:
        None
    """

    balance = np.array([])
    
    for i in range(num_plays):
        balance = np.append(balance, strategy(initial_balance, i, initial_bet, preference))


    # Plotting Configurations
    fig, ax = plt.subplots(figsize=(4,3))
    
    # Setting size 
    fig.set_size_inches(10,4)
    
    ax.plot(range(num_plays), balance)

    # Labels
    ax.set_title("Line Graph for Number of Plays vs. Ending Balance")
    ax.set_xlabel("Number of Plays")
    ax.set_ylabel("Ending Balance")
    ax.axhline(initial_balance, color='red', linestyle='--')
    ax.text(0, balance.max(), f'STARTING BALANCE: {initial_balance}', color='red')

    col1, col2 = st.columns([1, 1])
    with col1:
        st.pyplot(fig, use_container_width=True)