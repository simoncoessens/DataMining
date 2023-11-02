import pandas as pd
import folium
from shapely.geometry import Point
from geopandas import GeoDataFrame

# Define a filter fraction to remove entries from the DataFrame
filter_fraction = 10  # Removes 99/100 entries

# Load the CSV file
df = pd.read_csv("ar41_for_ulb.csv", delimiter=';')

# Create a new DataFrame with every filter_fraction'th entry
df = df.iloc[::filter_fraction]

# Convert timestamps to datetime
df['date'] = pd.to_datetime(df['timestamps_UTC'])

# Filter entries for the month of July
df = df[df['date'].dt.month == 7]

# Create a GeoDataFrame with Point geometries
geometry = [Point(xy) for xy in zip(df['lon'], df['lat'])]
gdf = GeoDataFrame(df, geometry=geometry)

# Calculate the map center based on the mean latitude and longitude
map_center = [df['lat'].mean(), df['lon'].mean()]

# Create a Folium map
m = folium.Map(location=map_center, zoom_start=12)

# Add CircleMarkers for each row in the GeoDataFrame
for _, row in gdf.iterrows():
    popup_text = f"Vehicle ID: {row['mapped_veh_id']}"
    folium.CircleMarker(
        location=[row['geometry'].y, row['geometry'].x],
        radius=1,
        popup=popup_text,
        color='blue',
        fill=True,
        fill_color='blue'
    ).add_to(m)

# Save the map as an HTML file
m.save("vehicle_map.html")