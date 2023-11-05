import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
from geopandas import GeoDataFrame
import matplotlib.pyplot as plt
import folium
import requests
from scipy.spatial import cKDTree

# Import file with locations of all weather stations
ws = pd.read_csv('grid_points_bel.csv')

# Create a GeoDataFrame from the weather station data
geometry = [Point(lon, lat) for lon, lat in zip(ws['lon'], ws['lat'])]
crs = {'init': 'epsg:4326'}
gdf = gpd.GeoDataFrame(ws, crs=crs, geometry=geometry)

# Loop for json requests
weather = pd.DataFrame()
for index, row in ws.iterrows():
    url = 'https://archive-api.open-meteo.com/v1/era5?latitude='+str(row['lat'])+'&longitude='+str(row['lon'])+'&start_date=2023-01-01&end_date=2023-09-13&hourly=temperature_2m'
    response = requests.get(url)
    if response.status_code == 200:
        data_aux = pd.DataFrame({"ID": row['id'], "Lat": row['lat'], "Lon": row['lon'], "Time": response.json()["hourly"]["time"], "Temperature": response.json()["hourly"]["temperature_2m"]})
        weather = pd.concat([weather, data_aux])
    else:
        print('Error')

# Change weather timestamps to datetime
weather['Time'] = pd.to_datetime(weather['Time'])

# Input csv file for the complete dataset
df = pd.read_csv('ar41_for_ulb_mini.csv', delimiter=';')
df['timestamps_UTC'] = pd.to_datetime(df['timestamps_UTC'])

# Get floor of hour
df['timestamps_floor'] = df['timestamps_UTC'].dt.floor('H')

# Create a cKDTree from the weather coordinates for fast spatial queries
weather_tree = cKDTree(gdf[['lon', 'lat']])

# Find the nearest weather station for each train timestamp
df['nearest_point_idx'] = [weather_tree.query((lon, lat))[1] for lon, lat in zip(df['lon'], df['lat'])]

# Merge with weather data based on the nearest point index
wdf = pd.merge(df, weather, how='left', left_on=['timestamps_floor', 'nearest_point_idx'], right_on=['Time', 'ID'])

wdf.to_csv('prueba2.csv', sep='\t')