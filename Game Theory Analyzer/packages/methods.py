import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

"""
Contains some universal methods that we can use for simulations, think of this like a module/dependency/library that we made ourselves
"""

def sample(strategy, repeats, initial_balance, num_plays, initial_bet, preference):
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

def frequency_plot(df, initial_balance):
    """
    Creates a matplotlib plot that visualizes the returns based on user input
    Args:
        df (DataFrame): dataframe that we are plotting
        initial_balance (int or float): the initial balance based on user input
    Returns:
        None
    """
    
    # Plotting configurations
    fig, ax = plt.subplots(figsize=(5,1))
    ax.hist(x=df.get('Balance'))
    plt.xlabel('Ending Balance')
    plt.ylabel('Frequency')

    st.pyplot(fig)