import tkinter as tk
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
import gui

# Constants
FILE_NAME = 'Tinder.csv'

# Load the CSV data
data = pd.read_csv(FILE_NAME, delimiter=';')
data['Datum'] = pd.to_datetime(data['Datum'], format="%d.%m.%Y")

# Calculate the likeshare
data['likeshare'] = data['Likes'] / (data['Likes'] + data['Passes'])

# Create the GUI
window = gui.create_gui(data)

# Run the GUI application
window.mainloop()