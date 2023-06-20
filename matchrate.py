import pandas as pd

def calculate_match_rate(data):
    # Create a copy of the input DataFrame to avoid modifying the original data
    data_copy = data.copy()

    # Convert the "Datum" column to datetime objects
    data_copy['Datum'] = pd.to_datetime(data_copy['Datum'], format="%d.%m.%Y")

    # Set the "Datum" column as the index for the DataFrame
    data_copy.set_index('Datum', inplace=True)

    # Resample the data into 7-day periods and calculate the number of matches and likes in each period
    resampled_data = data_copy.resample('7D').agg({'swipes_likes': 'sum', 'matches': 'sum'})

    # Calculate the match rate as matches divided by likes, and add it as a new column in the DataFrame
    resampled_data['Match Rate'] = (resampled_data['matches'] / resampled_data['swipes_likes'])*100

    # Return the resulting DataFrame
    return resampled_data