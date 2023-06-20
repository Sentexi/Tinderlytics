import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def clear_plot_frame(plot_frame):
    for child in plot_frame.winfo_children():
        child.destroy()

def find_correlations(data, result_label, plot_frame):
    correlations = data.corr()
    result_label.config(text=correlations)

def create_histogram(data, plot_frame, x_label, y_label, title, likes_color="blue", passes_color="green", x_ticks_rotation=0):
    fig_size = (10, 6)

    # Clear any previous plot
    clear_plot_frame(plot_frame)

    # Create the histogram
    fig, ax = plt.subplots(figsize=fig_size)
    ax.plot(data[x_label], data["swipes_likes"], label="Likes", marker="o", linestyle="--", color=likes_color)
    ax.plot(data[x_label], data["swipes_passes"], label="Passes", marker="s", linestyle="-", color=passes_color)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.tick_params(axis='x', rotation=x_ticks_rotation)
    ax.legend()

    # Embed the plot in the GUI
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    # Pack the canvas into the given frame
    canvas.get_tk_widget().pack(fill='both', expand=True)

def create_7d_histogram(data, plot_frame):
    # Bin the data in intervals of 7 days
    data["Bins"] = data["Datum"].dt.floor("7D")

    # Group the data by bins and calculate the sum of likes and passes
    grouped_data = data.groupby("Bins").agg({"swipes_likes": "sum", "swipes_passes": "sum"}).reset_index()

    # Create the histogram using different colors for likes and passes
    create_histogram(grouped_data, plot_frame, "Bins", "Likes and Passes per 7-day Interval", "Likes and Passes per 7-day Interval", likes_color="blue", passes_color="green", x_ticks_rotation=45)


def create_30d_histogram(data, plot_frame):
    # Bin the data in intervals of 30 days
    data["Bins"] = data["Datum"].dt.floor("30D")

    # Group the data by bins and calculate the sum of likes and passes
    grouped_data = data.groupby("Bins").agg({"swipes_likes": "sum", "swipes_passes": "sum"}).reset_index()

    # Create the histogram using different colors for likes and passes
    create_histogram(grouped_data, plot_frame, "Bins", "Likes and Passes per 30-day Interval", "Likes and Passes per 30-day Interval", likes_color="blue", passes_color="green", x_ticks_rotation=45)

def create_7d_matchrate_histogram(data, plot_frame):
    # Resample the data into 7-day periods
    data_7d = data.resample('7D').mean()
    
    #print(data_7d.head())

    # Create a time series plot of the match rate, likes, and passes data using Matplotlib
    fig, ax1 = plt.subplots(figsize=(6, 4), dpi=100)
    ax2 = ax1.twinx()

    # Plot match rates as a blue bar chart on the left y-axis
    ax1.bar(data_7d.index, data_7d['Match Rate'], width=5.0, color='blue', label='Match Rate')
    ax1.set_ylabel('Match Rate', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Plot likes as a green line on the right y-axis
    ax2.plot(data_7d.index, data_7d['swipes_likes'], color='green', label='Likes')
    ax2.set_ylabel('Likes', color='green')
    ax2.tick_params(axis='y', labelcolor='green')

    # Set plot labels and legend
    ax1.set_xlabel('Date')
    ax1.set_title('7-Day Tinder Histogram')
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    # Add gridlines
    ax1.grid(True)

    # Embed the plot in the GUI using a FigureCanvasTkAgg object
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()

    # Pack the canvas into the given frame
    canvas.get_tk_widget().pack(fill='both', expand=True)