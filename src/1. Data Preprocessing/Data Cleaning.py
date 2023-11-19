import pandas as pd

# Reading the dataset into a DataFrame called 'df'
df = pd.read_csv(r"E:\Study\BDMA\ULB\Data Mining\SNCB Project\Dataset\ar41_for_ulb.csv", delimiter=';')

# Convert the 'timestamps_UTC' column to a datetime format
df['timestamps_UTC'] = pd.to_datetime(df['timestamps_UTC'])

# Filter the data to keep only records from 2023 and exclude those after September 2023
filtered_data = df[(df['timestamps_UTC'].dt.year == 2023) & (df['timestamps_UTC'].dt.month <= 9)]

# Drop rows where any of the elements is NAN
filtered_data = filtered_data.dropna()

# Coordinates to be removed
coordinates_to_remove = [
    (52.8570588, 4.4855411),
    (50.330024, 0.1750491),
    (50.3979063, 0.2067928),
    (49.3835907, 3.7002351),
    (49.7800844, 3.7347805)
]

# Remove rows with these coordinates
for lat, lon in coordinates_to_remove:
    filtered_data = filtered_data[~((filtered_data['lat'] == lat) & (filtered_data['lon'] == lon))]

# If you want to save the cleaned data:
filtered_data.to_csv("path_to_save_cleaned_data.csv", index=False)

print(filtered_data.head())