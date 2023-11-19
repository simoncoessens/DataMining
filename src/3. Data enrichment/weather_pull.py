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

weather.to_csv('weather_pull.csv', sep='\t')