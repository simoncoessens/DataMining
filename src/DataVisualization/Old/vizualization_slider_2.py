import pandas as pd
import folium
from shapely.geometry import Point
from geopandas import GeoDataFrame
from folium.plugins import TimestampedGeoJson
import random

# Define a filter fraction to remove entries from the DataFrame
filter_fraction = 1  # Removes 9/10 entries
mapped_veh_id = 181
day = 1
month = 8

# Load the CSV file
df = pd.read_csv("ar41_for_ulb.csv", delimiter=';')

# Filter out based on mapped_veh_id
# df = df[df['mapped_veh_id'] == mapped_veh_id]

# Convert timestamps to datetime
df['date'] = pd.to_datetime(df['timestamps_UTC'])

# Filter entries for the specified day and month
df = df[(df['date'].dt.month == month) & (df['date'].dt.day == day)]

# Sort the DataFrame based on the 'date' column
df = df.sort_values(by='date')

# Reset the index for the sorted DataFrame
df = df.reset_index(drop=True)

# Create a new DataFrame with every filter_fraction'th entry
# df = df.iloc[::filter_fraction]

# Create a color map and assign each 'mapped_veh_id' to a unique hex color
color_map = {}
unique_vehicle_ids = df['mapped_veh_id'].unique()
for veh_id in unique_vehicle_ids:
    # Generate a random hexadecimal color
    color = "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    color_map[veh_id] = color

# Create a GeoDataFrame with Point geometries
geometry = [Point(xy) for xy in zip(df['lon'], df['lat'])]
gdf = GeoDataFrame(df, geometry=geometry)

# Calculate the map center based on the mean latitude and longitude
map_center = [df['lat'].mean(), df['lon'].mean()]

# Create a Folium map
m = folium.Map(location=map_center, zoom_start=12)

# Prepare data for the TimestampedGeoJson
features = []

for idx, row in gdf.iterrows():
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [row['geometry'].x, row['geometry'].y],
        },
        "properties": {
            "time": row['date'].isoformat(),
            "popup": f"Vehicle ID: {row['mapped_veh_id']}",
            "id": f"vehicle-{row['mapped_veh_id']}",
            "icon": "circle",
            "iconstyle": {
                "fillColor": color_map.get(row['mapped_veh_id'], '#808080'),
                "fillOpacity": 0.6,
                "stroke": "false",
                "radius": 10,
            },
        },
    }
    features.append(feature)

# Add the TimestampedGeoJson to the map with a period of 2 minutes
TimestampedGeoJson(
    {
        "type": "FeatureCollection",
        "features": features,
    },
    period="PT2M",
    add_last_point=False,
    duration="PT1M"
).add_to(m)

# Name the HTML file dynamically based on 'mapped_veh_id'
html_file_name = f'vehicle_slider_map_color_1aug.html'

# Save the map as the dynamically named HTML file
m.save(html_file_name)