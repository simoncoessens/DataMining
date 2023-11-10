#import psycopg2
import pandas as pd
import plotly.graph_objects as go
from sqlalchemy import create_engine

# Database connection parameters
dbname = 'DataMining'
user = 'postgres'
password = 'datamining'
host = 'localhost'  # localhost or the server address
port = '5433'  # default PostgreSQL port is 5432
vehicle_id = 181  # Replace with the vehicle ID you are interested in

# SQL query to select data for a specific vehicle ID sorted by timestamp
query = f"""
SELECT * FROM vehicle_data 
WHERE mapped_veh_id = {vehicle_id} 
ORDER BY timestamps_UTC;
"""

# Establish a connection to the database
#conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
connection_str  = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

# Create the engine
engine = create_engine(connection_str)

# Use the engine to connect and execute queries
query = "SELECT * FROM vehicle_data WHERE mapped_veh_id = %s ORDER BY timestamps_utc;"
df = pd.read_sql_query(query, engine, params=(vehicle_id,))

# Don't forget to close the engine connection when done
engine.dispose()

# Convert timestamps to datetime
df['timestamps_utc'] = pd.to_datetime(df['timestamps_utc'])

# Calculate time differences between consecutive rows
df['time_diff'] = df['timestamps_utc'].diff()

# Define a journey as a period where consecutive data points are no more than 5 minutes apart
journey_gap = pd.Timedelta(minutes=5)

# Identify journeys by checking where the time difference is greater than 5 minutes
df['journey'] = (df['time_diff'] > journey_gap).cumsum()

# Now, df['journey'] labels each row with a journey number
# We can partition the DataFrame into a list of DataFrames, each containing a continuous journey
journeys = [journey_data for _, journey_data in df.groupby('journey')]

for i, journey in enumerate(journeys, start=1):
    # Assuming 'timestamps_utc' are in datetime format; if not, convert them first
    start_time = pd.to_datetime(journey['timestamps_utc'].iloc[0])
    end_time = pd.to_datetime(journey['timestamps_utc'].iloc[-1])
    duration = end_time - start_time
    print(f"Journey {i}, Start Time: {start_time}, End Time: {end_time}, Duration: {duration}")