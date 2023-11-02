import pandas as pd
import folium
from shapely.geometry import Point
from geopandas import GeoDataFrame

# Define a filter fraction to remove entries from the DataFrame
filter_fraction = 100  # Removes 99/100 entries
mapped_veh_id = 181

# Load the CSV file
df = pd.read_csv("ar41_for_ulb.csv", delimiter=';')

# Filter out based on mapped_veh_id
df = df[df['mapped_veh_id'] == mapped_veh_id]

# Convert timestamps to datetime
df['date'] = pd.to_datetime(df['timestamps_UTC'])

# Sort the DataFrame based on the 'date' column
df = df.sort_values(by='date')

# Reset the index for the sorted DataFrame
df = df.reset_index(drop=True)

# Create a new DataFrame with every filter_fraction'th entry
df = df.iloc[::filter_fraction]

print("Number of rows", df.count())

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

# Add service stations in the map plot
ss = pd.read_csv("service_stations_SCNB.csv")

# Create a GeoDataFrame with Point geometries for the service stations
ssgeo = [Point(xy) for xy in zip(ss['Lon'], ss['Lat'])]
ss_gdf = GeoDataFrame(ss, geometry=ssgeo)

# Add CircleMarkers for each row in the new GeoDataFrame (Service Stations)
for _, row in ss_gdf.iterrows():
    popup_text = f"ID: {row['ID']}"
    folium.CircleMarker(
        location=[row['geometry'].y, row['geometry'].x],
        radius=1,
        popup=popup_text,
        color='red',  # Use a different color, e.g., red
        fill=True,
        fill_color='red'
    ).add_to(m)

# Name the HTML file dynamically based on 'mapped_veh_id'
html_file_name = f'vehicle_map_{mapped_veh_id}_w_ss.html'

# Save the map as the dynamically named HTML file
m.save(html_file_name)