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
wsdf = pd.DataFrame(ws)

# Create a GeoDataFrame from the pull request data
geometry = [Point(lon, lat) for lon, lat in zip(wsdf['lon'], ws['lat'])]
crs = {'init': 'epsg:4326'}
gdf = gpd.GeoDataFrame(wsdf, crs=crs, geometry=geometry)

# Loop for json requests
weather = pd.DataFrame()
for index, row in ws.iterrows():
    url = 'https://archive-api.open-meteo.com/v1/era5?latitude='+str(row['lat'])+'&longitude='+str(row['lon'])+'&start_date=2023-01-01&end_date=2023-09-13&hourly=temperature_2m,relative_humidity_2m,rain'
    response = requests.get(url)
    if response.status_code == 200:
        data_aux = pd.DataFrame({"ID": row['id'], "Lat": row['lat'], "Lon": row['lon'], "Time": response.json()["hourly"]["time"], "Temperature": response.json()["hourly"]["temperature_2m"], "Humidity": response.json()["hourly"]["relative_humidity_2m"], "Rain": response.json()["hourly"]["rain"]})
        weather = pd.concat([weather, data_aux])
    else:
        print('Error')

# Change weather timestamps to datetime
weather['Time'] = pd.to_datetime(weather['Time'])

# Input csv file for the complete dataset
df = pd.read_csv('ar41_for_ulb.csv', delimiter=';')
df['timestamps_UTC'] = pd.to_datetime(df['timestamps_UTC'])

# Get floor of hour
df['timestamps_floor'] = df['timestamps_UTC'].dt.floor('H')

# cKDTree from the weather coordinates to perform spatial queries
weather_tree = cKDTree(gdf[['lon', 'lat']])

# Find the nearest weather point for each train timestamp
nearest_indices = [weather_tree.query((lon, lat))[1] for lon, lat in zip(df['lon'], df['lat'])]
df['nearest_point_id'] = gdf['id'].iloc[nearest_indices].to_list()

# Merge with weather data based on the nearest point index
wdf = pd.merge(df, weather, how='left', left_on=['timestamps_floor', 'nearest_point_id'], right_on=['Time', 'ID'])
wdf = wdf.drop(columns=['Unnamed: 0', 'ID'])

wdf.to_csv('ar41_weather.csv', sep='\t')