import numpy as np
import pandas as pd

"""
Contains methods for data manipulation
"""

def sample(strategy, repeats, initial_balance, num_plays, initial_bet, preference, target_balance, floor_balance):
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
        arr = np.append(arr, strategy(initial_balance, num_plays, initial_bet, preference, target_balance, floor_balance))
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