import os
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import pandas as pd
import matplotlib.pyplot as plt
from methods import(
    find_correlations,
    create_7d_histogram,
    create_30d_histogram,
    clear_plot_frame,
    create_7d_matchrate_histogram,
)
import matchrate
import load_data

# Constants
WINDOW_TITLE = 'Data Exploration'
WINDOW_SIZE = '800x600'

# Check if the folder 'Data' exists, and create it if it doesn't
if not os.path.exists('Data'):
    os.makedirs('Data')

def calc_gui(selected_folder):
    data = load_data.load(selected_folder)

    # Create GUI window
    window = tk.Tk()
    window.title(WINDOW_TITLE)
    window.geometry(WINDOW_SIZE)
    #window.attributes('-fullscreen', True)  # Open the GUI in full-screen mode

    # Create the frame for the plot
    plot_frame = tk.Frame(window)
    plot_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Button actions
    def display_correlation():
        correlations = data.corr()
        lbl_result.config(text=correlations)
        find_correlations(data, lbl_result, plot_frame)

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

    return window
    

def explorer_gui():
    def open_selected_item(event):
        selected_item = tree.focus()
        if selected_item:
            item_type = tree.item(selected_item)['values'][1]
            if item_type == 'Folder':
                folder_path = tree.item(selected_item)['values'][0]
                open_second_gui(folder_path)

    def browse_directory(folder_path='Data'):
        tree.delete(*tree.get_children())  # Clear the treeview
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                tree.insert('', 'end', text=item, values=(item_path, 'Folder'))

    def open_second_gui(selected_folder):
        window.destroy()  # Hide the first GUI window
        calc_gui(selected_folder)


    window = tk.Tk()
    window.title('Explorer')
    window.geometry('600x400')

    # Create the treeview widget
    tree = ttk.Treeview(window)
    tree.pack(fill=tk.BOTH, expand=True)
    tree.bind('<<TreeviewSelect>>', open_selected_item)

    # Create the columns
    tree['columns'] = ('path', 'type')
    tree.column('path', width=300)
    tree.column('type', width=50)

    # Define the column headings
    tree.heading('#0', text='Name')
    tree.heading('path', text='Path')
    tree.heading('type', text='Type')

    # Automatically browse the "Data" folder
    browse_directory()

    window.mainloop()