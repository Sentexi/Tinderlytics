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

# Create and run the GUI
window = gui.explorer_gui()