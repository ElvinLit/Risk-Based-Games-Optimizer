import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

def roulette_plot(line_plot, frequency_plot, box_plot, stats_table):
    """
    Plots all the graphs for the roulette strategies
    Args:
        line_plot ('fig' object): Line plot information
        frequency_plot ('fig' object): Frequency plot information
        box_plot ('fig' object): Box plot information
    Returns:
        None
    """
    # Assigning statistical data

    col1, col2 = st.columns([1, 1])
    with col1:
        st.pyplot(line_plot, use_container_width=True)
        tooltip_css1 = """
        .tooltip1 {
        position: relative;
        display: block;
        }

        .tooltip1::after {
        content: "This graph is a scatterplot that reveals various ending balances that occured in samples with the corresponding number of plays";
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        background-color: #333;
        color: #fff;
        padding: 5px;
        border-radius: 5px;
        font-size: 12px;
        opacity: 0;
        visibility: hidden;
        transition: opacity 0.2s, visibility 0.2s;
        }

        .tooltip1:hover::after {
        opacity: 1;
        visibility: visible;
        }
        """

        # Add the CSS to the Streamlit app
        st.markdown(f'<style>{tooltip_css1}</style>', unsafe_allow_html=True)

        # Add the tooltip-like element
        st.markdown('<div class="tooltip1">Info</div>', unsafe_allow_html=True)
    with col2:
        st.pyplot(frequency_plot, use_container_width=True)
        tooltip_css2 = """
        .tooltip2 {
        position: relative;
        display: block;
        }

        .tooltip2::after {
        content: "This graph is a histogram that displays the frequency of each ending balance amount of the sample repititions";
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        background-color: #333;
        color: #fff;
        padding: 5px;
        border-radius: 5px;
        font-size: 12px;
        opacity: 0;
        visibility: hidden;
        transition: opacity 0.2s, visibility 0.2s;
        }

        .tooltip2:hover::after {
        opacity: 1;
        visibility: visible;
        }
        """

        # Add the CSS to the Streamlit app
        st.markdown(f'<style>{tooltip_css2}</style>', unsafe_allow_html=True)

        # Add the tooltip-like element
        st.markdown('<div class="tooltip2">Info</div>', unsafe_allow_html=True)
    col3, col4 = st.columns([1, 1])
    with col3:
        st.pyplot(box_plot, use_container_width=True)
        tooltip_css3 = """
        .tooltip3 {
        position: relative;
        display: block;
        }

        .tooltip3::after {
        content: "This graph is a box and whisker plot that denotes the descriptive statistics of all samples in one run of the algorithm based on parameters set by the user.";
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        background-color: #333;
        color: #fff;
        padding: 5px;
        border-radius: 5px;
        font-size: 12px;
        opacity: 0;
        visibility: hidden;
        transition: opacity 0.2s, visibility 0.2s;
        }

        .tooltip3:hover::after {
        opacity: 1;
        visibility: visible;
        }
        """

        # Add the CSS to the Streamlit app
        st.markdown(f'<style>{tooltip_css3}</style>', unsafe_allow_html=True)

        # Add the tooltip-like element
        st.markdown('<div class="tooltip3">Info</div>', unsafe_allow_html=True)       
    with col4:
        st.markdown(stats_table, unsafe_allow_html=True)
    
def styling_configurations(fig, ax):
    """
    Contains all the styling information for our plots
    """

    # Setting grid style
    plt.style.use('seaborn-whitegrid')
    plt.rcParams['grid.alpha'] = 0.3

    # Setting fonts
    
    plt.rcParams['font.family'] = 'monospace'

    fig.set_facecolor('none')
    ax.set_facecolor("none")

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


def frequency_plot(df, initial_balance, repeats, graph_width):
    """
    Creates a frequency plot that visualizes the returns based on user input
    Args:
        df (DataFrame): dataframe that we are plotting
        initial_balance (int or float): the initial balance based on user input
    Returns:
        'fig' object: contains information about our frequency plot
    """
    
    # Plotting configurations
    fig, ax = plt.subplots()
    styling_configurations(fig, ax)
    
    # Setting size 
    fig.set_size_inches(10,4)

    # Setting range for our graph
    lower_range = df['Balance'].mean() - graph_width
    upper_range = df['Balance'].mean() + graph_width

    # Setting general colors and title
    ax.hist(df['Balance'], bins=50, range=(lower_range, upper_range), color='white', edgecolor='black')

    # Labels
    ax.set_title("Frequency Histogram of different Returns, n = " + str(repeats), color = 'white')
    ax.set_xlabel("Ending Balance", color = 'white')
    ax.set_ylabel("Frequency", color = 'white')
    ax.axvline(x=initial_balance, color='red', linestyle='--')
    for label in ax.get_xticklabels():
        label.set_color('white')
    for label in ax.get_yticklabels():
        label.set_color(color = 'white')

    # Calculating annotation location
    hist, bin_edges = np.histogram(df['Balance'], bins=50, range=(lower_range, upper_range))
    filtered_hist = hist[(bin_edges[:-1] >= lower_range) & (bin_edges[1:] <= upper_range)]

    ax.annotate(f'STARTING BALANCE: {initial_balance}', xy=(initial_balance, 0), xytext=(initial_balance, np.mean(filtered_hist)),
             arrowprops=dict(arrowstyle='->', color = "Red"), color = "Red")

    return fig

def line_plot(strategy, num_plays, initial_balance, initial_bet, preference, target_balance):
    """
    Creates a line plot that visualizes the returns vs number of plays
    Args:
       Args:
        df (DataFrame): dataframe that we are plotting
        num_plays (int): number of plays
        initial_balance (int or float): the initial balance based on user input
        initial_bet (int or float): starting amount
        preference (string): Color preference from "red", "black", or "green"

    Returns:
        'fig' object: contains information about our frequency plot
    """

    # Generating our samples
    balance = np.array([])
    for i in range(num_plays):
        balance = np.append(balance, strategy(initial_balance, i, initial_bet, preference, target_balance))

    # Plotting Configurations
    fig, ax = plt.subplots()
    
    styling_configurations(fig, ax)
    
    # Setting size 
    fig.set_size_inches(10,4)
    
    # Labels
    ax.set_title("Scatterplot for Number of Plays vs. Ending Balance", color = 'white')
    ax.set_xlabel("Number of Plays", color = 'white')
    ax.set_ylabel("Ending Balances", color = 'white')
    ax.axhline(initial_balance, color='red', linestyle='--')
    
    styling_configurations(fig, ax)
    for label in ax.get_xticklabels():
        label.set_color('white')
    for label in ax.get_yticklabels():
        label.set_color(color = 'white')
    ax.text(0, balance.max(), f'STARTING BALANCE: {initial_balance}', color='red')

    ax.scatter(range(num_plays), balance, color = 'white')

    return fig

def box_plot(df, initial_balance, repeats, graph_width):
    """
    Creates a box plot that visualizes the returns based on user input
    Args:
        df (DataFrame): dataframe that we are plotting
        initial_balance (int or float): the initial balance based on user input
    Returns:
        'fig' object: contains information about our box plot
    """
    
    # Plotting configurations
    fig, ax = plt.subplots()
    styling_configurations(fig, ax)
    
    # Setting size 
    fig.set_size_inches(10,4)

    # Setting range for our graph
    lower_range = df['Balance'].mean() - graph_width
    upper_range = df['Balance'].mean() + graph_width

    # Setting general colors and title
    ax.boxplot(df['Balance'], boxprops=dict(color='white'), whiskerprops=dict(color='white'), capprops=dict(color='white'), medianprops=dict(color='white'), flierprops=dict(marker='o', markersize=6, markerfacecolor='white'), vert=False)
    ax.set_xlabel('Data')
    ax.set_ylabel('Values')
    ax.set_title('Box Plot')
    
    # Labels
    ax.set_title("Box Plot of different Returns, n = " + str(repeats), color = 'white')
    ax.set_xlabel("Ending Balances", color = 'white')
    ax.set_ylabel("", color = 'white')
    ax.axvline(initial_balance, color='red', linestyle='--')
    ax.set_yticks([])
    for label in ax.get_xticklabels():
        label.set_color('white')

    # Calculating annotation location
    hist, bin_edges = np.histogram(df['Balance'], bins=50, range=(lower_range, upper_range))
    filtered_hist = hist[(bin_edges[:-1] >= lower_range) & (bin_edges[1:] <= upper_range)]

    ax.annotate(f'STARTING BALANCE: {initial_balance}', xy=(initial_balance, 0), xytext=(initial_balance, np.mean(filtered_hist)),
             arrowprops=dict(arrowstyle='->', color = "Red"), color = "Red")
    
    max = df['Balance'].max()
    median = df['Balance'].median()
    first_quartile = df['Balance'].quantile(0.25)
    third_quartile = df['Balance'].quantile(0.75)

    ax.annotate(f'Median: {median:.2f}', xy=(median, 1), xytext=(median, 1.2), arrowprops=dict(arrowstyle='->', color='Red'), color='white')

    return fig

def stats_table(df, initial_balance):
    """
    Creates a table that relays all the statistics associated with the parameters input
    Args:
        df (DataFrame): dataframe that we are plotting

    Returns:
        'fig' object: table that displays all the stats
    """
    mean = round(df['Balance'].mean(), 2)
    median = df['Balance'].median()
    max = df['Balance'].max()
    min = df['Balance'].min()
    stdev = round(df['Balance'].std(), 2)
    mode = df['Balance'].mode().iloc[0]
    percentage_win = df[df['Balance'] >= initial_balance].shape[0] / df.shape[0] * 100
    percentage_win_str = f"{percentage_win:.2f}%"
    percentage_lose = df[df['Balance'] < initial_balance].shape[0] / df.shape[0] * 100
    percentage_lose_str = f"{percentage_lose:.2f}%"
    
    # Setting up data text
    stats_table = f"""
    <center>

    **Descriptive Statistics**

    |                    |                         |
    |--------------------|-------------------------|
    | **Mean**           | {mean}                  |
    | **Median**         | {median}                |
    | **Max**            | {max}                   |
    | **Min**            | {min}                   |
    | **Mode**           | {mode}                  |
    | **Standard Deviation** | {stdev}            |
    | **Chance of gaining money** | {percentage_win} |
    | **Chance of losing money**  | {percentage_lose} |

    </center>
    """

    return stats_table




