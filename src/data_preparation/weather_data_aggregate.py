import pandas as pd
from pathlib import Path

# define paths
project_root = Path(__file__).resolve().parents[2]
input_path = project_root / 'data/raw data/weather-data_2025_prep.csv'
output_path = project_root / 'data/clean data/weather-data_2025.csv'

# read 1st csv-file
df = pd.read_csv(input_path)

# group by 'timestamp', calculate and round mean of 'temperature_2m' and 'shortwave_radiation' to 4 decimals
df_avg = df.groupby('timestamp')[['temperature_2m', 'shortwave_radiation']].mean().round(4).reset_index()

# create new csv-file and save changes
df_avg.to_csv(output_path, index=False)