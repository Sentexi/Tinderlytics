import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from methods import(
    find_correlations,
    create_7d_histogram,
    create_30d_histogram,
    clear_plot_frame,
    create_7d_matchrate_histogram,
)
import matchrate
import pandas as pd
import matplotlib.pyplot as plt

# Constants
FILE_NAME = 'Tinder.csv'
WINDOW_TITLE = 'Data Exploration'
WINDOW_SIZE = '800x600'

# Load the CSV data
data = pd.read_csv(FILE_NAME, delimiter=';')
data['Datum'] = pd.to_datetime(data['Datum'], format="%d.%m.%Y")

# Calculate the likeshare
data['likeshare'] = data['Likes'] / (data['Likes'] + data['Passes'])

# Create GUI window
window = tk.Tk()
window.title(WINDOW_TITLE)
window.geometry(WINDOW_SIZE)
window.attributes('-fullscreen', True)  # Open the GUI in full-screen mode

# Create the frame for the plot
plot_frame = tk.Frame(window)
plot_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)


# Button actions
def display_correlation():
    correlations = data.corr()
    lbl_result.config(text=correlations)
    find_correlations(data, lbl_result, plot_frame)
    
# Define the function to display the 7-day match rate histogram
def display_7day_matchrate_histogram():
    clear_plot_frame(plot_frame)
    # Load the data from the file
    data2 = data.copy()

    # Call the calculate_match_rate function from matchrate.py to calculate the match rate
    match_rate = matchrate.calculate_match_rate(data2)

    # Call create_7d_matchrate_histogram function from methods.py to create the histogram
    create_7d_matchrate_histogram(match_rate, plot_frame)
    
def display_7day_histogram():
    clear_plot_frame(plot_frame)
    
    create_7d_histogram(data, plot_frame)

def display_30day_histogram():
    clear_plot_frame(plot_frame)
    
    create_30d_histogram(data, plot_frame)

def calculate_total_swipes():   
    global data
    data = calculate_total_swipes(data)

def close_window():
    window.destroy()
    
# Helper function to destroy plots
def destroy_plots():
    plt.close('all')

# Create GUI elements
btn_frame = tk.Frame(window)
btn_frame.pack(pady=20)

btn_correlation = ttk.Button(btn_frame, text="Find Correlations", command=display_correlation)
btn_correlation.pack(side=tk.LEFT, padx=10)

btn_histogram_7d = ttk.Button(btn_frame, text="Create 7D Histogram", command=display_7day_histogram)
btn_histogram_7d.pack(side=tk.LEFT, padx=10)

btn_histogram_30d = ttk.Button(btn_frame, text="Create 30D Histogram", command=display_30day_histogram)
btn_histogram_30d.pack(side=tk.LEFT, padx=10)

btn_calculate = ttk.Button(btn_frame, text="Calculate Swipes", command=calculate_total_swipes)
btn_calculate.pack(side=tk.LEFT, padx=10)

btn_exit = ttk.Button(window, text="Exit App", command=close_window)
btn_exit.pack(side=tk.BOTTOM, pady=20)

# Create the button to display the 7-day match rate histogram
btn_matchrate_histogram = ttk.Button(btn_frame, text="Calculate Match Rate Histogram", command=display_7day_matchrate_histogram)
btn_matchrate_histogram.pack(side=tk.LEFT, padx=10)

lbl_result = ttk.Label(window, text="")
lbl_result.pack()

# Run the GUI application
window.mainloop()