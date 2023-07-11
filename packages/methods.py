import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

"""
Contains some universal methods that we can use for simulations, think of this like a module/dependency/library that we made ourselves
"""

def sample(strategy, repeats, initial_balance, num_plays, initial_bet, preference, target_balance = None):
    """
    Returns array of numbers collected from simulation
    Args:
        strategy (function): strategy used
        repeats (int): amount of samples we want
        starting_balance (int or float): Starting amount
        num_plays (int): Number of plays
        initial_bet (int or float): Starting amount
        preference (string): Color preference from "Red", "Black", or "Green"
    Returns: 
        array: aggregation of our simulations
    """
    arr = np.array([])
    for _ in range(repeats):
        arr = np.append(arr, strategy(initial_balance, num_plays, initial_bet, preference))
    return arr

def dataframe_conversion(samples):
    """
    Returns a pandas 'DataFrame' object that contains 2 columns, the first being the index and the second being 'Balance' with the array of 'samples'
    Args:
        samples (np.array): array of samples collected from a strategy
    Returns: 
        pd.DataFrame: dataframe with our samples as a column
    """
    return pd.DataFrame(samples, columns=['Balance'])

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
    ax.hist(df['Balance'], bins=50, range=(lower_range, upper_range), color='cyan', edgecolor='cyan')
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
    ax.set_yticklabels(ax.get_yticks(), color = 'white')
    ax.set_xticklabels(ax.get_yticks(), color = 'white')
    '''
    for label in ax.get_xticklabels():
        label.set_color('white')
    for label in ax.get_yticklabels():
        label.set_color('white')
    '''
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