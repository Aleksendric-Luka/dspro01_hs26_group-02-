import csv
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

# Define paths relative to the project folder
# This script is located in src/data_preparation/
project_root = Path(__file__).resolve().parents[2]
input_path, output = project_root / 'data/raw data/weather-data_2025.json', project_root / 'data/raw data/weather-data_2025.json'
output_path = output.with_name('weather-data_2025_prep.csv')

# Load JSON file
with input_path.open(encoding='utf-8-sig') as file:
    data = json.load(file)

# Treat a single location as a list as well
if isinstance(data, dict):
    data = [data]

zurich = ZoneInfo('Europe/Zurich')
rows = []

# Iterate through each location and extract hourly data
for i, location_data in enumerate(data):
    hourly = location_data['hourly']

    # Read the fixed UTC offset used by the API for this location
    source_timezone = timezone(
        timedelta(seconds=location_data['utc_offset_seconds'])
    )

    # Keep weather variables; coordinates are not included in the output
    variables = [name for name in hourly
                 if name not in ('time', 'latitude', 'longitude', 'location_index')]

    for j, time in enumerate(hourly['time']):
        # Assign the API offset, then convert to Zurich summer/winter time
        timestamp = datetime.fromisoformat(time)
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=source_timezone)
        timestamp = timestamp.astimezone(zurich)

        # Rename time to timestamp and include seconds and the correct offset
        row = {'timestamp': timestamp.isoformat(timespec='seconds')}

        # Keep all weather values and identify the location by its index
        for variable in variables:
            row[variable] = hourly[variable][j]
        row['location_index'] = i
        rows.append(row)

# Save all locations as one CSV file; no rows are removed
with output_path.open('w', encoding='utf-8', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f'Gespeichert: {output_path} ({len(rows)} Zeilen)')
