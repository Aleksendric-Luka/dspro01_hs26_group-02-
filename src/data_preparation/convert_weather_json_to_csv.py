import json
import pandas as pd

# Load json file
with open('data/weather-data_2025.json', 'r') as file:
    data = json.load(file)

df_list = []

# iterate through each location and extract hourly data
for i, location_data in enumerate(data):
    # extracts time, temperature_2m, and shortwave_radiation into columns
    df_location = pd.DataFrame(location_data['hourly'])

    # identify location by its index (0 to 6) and coordinates
    df_location['location_index'] = i
    df_location['latitude'] = location_data['latitude']
    df_location['longitude'] = location_data['longitude']

    df_list.append(df_location)

# concatenate all location DataFrames into one single table
df_combined = pd.concat(df_list, ignore_index=True)

# save as csv file
df_combined.to_csv('data/weather-data_2025.csv', index=False)