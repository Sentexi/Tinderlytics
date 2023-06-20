import pandas as pd
import os

def load(selected_folder):
    # Constants
    FILE_NAME = 'Tinder.csv'
    PATH_TO_FILE = os.path.join(selected_folder,FILE_NAME)

    # Load the CSV data
    data = pd.read_csv(PATH_TO_FILE, delimiter=',')
    # Convert the 'Datum' column to datetime format
    data['Datum'] = pd.to_datetime(data['Datum'], format="%Y-%m-%d")

    # Calculate the likeshare
    data['likeshare'] = data['swipes_likes'] / data['total_swipes']
    return data