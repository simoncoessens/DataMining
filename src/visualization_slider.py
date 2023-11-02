import pandas as pd
import folium
from shapely.geometry import Point
from geopandas import GeoDataFrame
from folium.plugins import TimestampedGeoJson

# Define a filter fraction to remove entries from the DataFrame
filter_fraction = 1  # Removes 9/10 entries
mapped_veh_id = 181

# Load the CSV file
df = pd.read_csv("ar41_for_ulb.csv", delimiter=';')

# Filter out based on mapped_veh_id
#df = df[df['mapped_veh_id'] == mapped_veh_id]

# Convert timestamps to datetime
df['date'] = pd.to_datetime(df['timestamps_UTC'])

# Filter entries for the month of July
df = df[df['date'].dt.month == 7]

# Sort the DataFrame based on the 'date' column
df = df.sort_values(by='date')

# Reset the index for the sorted DataFrame
df = df.reset_index(drop=True)

# Create a new DataFrame with every filter_fraction'th entry
#df = df.iloc[::filter_fraction]

# Create a GeoDataFrame with Point geometries
geometry = [Point(xy) for xy in zip(df['lon'], df['lat'])]
gdf = GeoDataFrame(df, geometry=geometry)

# Calculate the map center based on the mean latitude and longitude
map_center = [df['lat'].mean(), df['lon'].mean()]

# Create a Folium map
m = folium.Map(location=map_center, zoom_start=12)

# Prepare data for the TimestampedGeoJson
features = []
count = 0
for idx, row in gdf.iterrows():
    count += 1
    print(count)
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [row['geometry'].x, row['geometry'].y],
        },
        "properties": {
            "time": row['date'].isoformat(),
            "popup": f"Vehicle ID: {row['mapped_veh_id']}",
        },
    }
    features.append(feature)

# Add the TimestampedGeoJson to the map with a period of 10 minutes
TimestampedGeoJson(
    {
        "type": "FeatureCollection",
        "features": features,
    },
    period="PT1M",  # Change the time period to 10 minutes
    add_last_point=False,
    duration= "PT1M"
).add_to(m)

# Name the HTML file dynamically based on 'mapped_veh_id'
html_file_name = f'vehicle_slider_map_{mapped_veh_id}.html'

# Save the map as the dynamically named HTML file
m.save(html_file_name)