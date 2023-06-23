import os
import zipfile
import datetime
import pandas as pd
import json

def extract():
    # Function to create binned DataFrames
    def create_binned_dataframes(df):
        # Ensure the 'Date' column is in datetime format
        df['Datum'] = pd.to_datetime(df['Datum'])
        
        # Create 7-day DataFrame
        df_7D = df.groupby(pd.Grouper(key='Datum', freq='7D')).sum()
        
        # Create 30-day DataFrame
        df_30D = df.groupby(pd.Grouper(key='Datum', freq='30D')).sum()
        
        # Save the 7-day DataFrame to CSV
        df_7D.to_csv(f'{extraction_folder}/Tinder7D.csv')
        
        # Save the 30-day DataFrame to CSV
        df_30D.to_csv(f'{extraction_folder}/Tinder30D.csv')

    # Check if the zip file 'myData.zip' exists
    if os.path.exists('Data/myData.zip'):
        # Extract the zip file to a folder with the same name plus a timestamp
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y")
        extraction_folder = f'Data/myData_{timestamp}'
        with zipfile.ZipFile('Data/myData.zip', 'r') as zip_ref:
            zip_ref.extractall(extraction_folder)
            print(f'Extracted to: {extraction_folder}')
        
        # Access the "data.json" file and transform it into a Pandas DataFrame
        json_file_path = f'{extraction_folder}/data.json'
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            usage_data = data.get("Usage", {})
            df = pd.DataFrame.from_dict(usage_data, orient="columns")
            
            # Include the index in a separate column
            df.reset_index(inplace=True)
            df.rename(columns={"index": "Datum"}, inplace=True)
            
            # Append the "Swipes" column
            swipes_likes = df.get("swipes_likes", 0)
            swipes_passes = df.get("swipes_passes", 0)
            df["total_swipes"] = swipes_likes + swipes_passes
            
            
            # Save the DataFrame to a CSV file
            csv_file_path = f'{extraction_folder}/Tinder.csv'
            df.to_csv(csv_file_path, index=False)
            print(f'Saved DataFrame to CSV: {csv_file_path}')
            
            # Assuming df is the previously created DataFrame containing the 'Swipes' column
            create_binned_dataframes(df)
            os.remove('Data/myData.zip')
        else:
            print('JSON file does not exist.')
    else:
        print('Zip file does not exist.')