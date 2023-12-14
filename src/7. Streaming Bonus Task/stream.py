import streamlit as st  # web development
import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import time  # to simulate a real time data, time loop
import plotly.express as px  # interactive charts
from folium.plugins import HeatMap
from sqlalchemy import create_engine
from datetime import datetime, time as dt_time
import humanize
import folium
from streamlit_folium import folium_static

st.set_page_config(
    page_title='Real-Time SNCB Dashboard',
    page_icon='🚆',
    layout='wide'
)

# Database connection parameters
dbname = 'DataMining'
user = 'postgres'
password = 'datamining'
host = 'localhost'  # localhost or the server address
port = '5433'  # default PostgreSQL port is 5432

# Establish a connection to the database
connection_str = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
engine = create_engine(connection_str)

# Title for the date selection section
st.title("Select Date Range")

# Create two date input widgets for start and end dates
# Create two date input widgets for start and end dates
start_date = st.date_input("Start Date", value=datetime(2023, 1, 1))
end_date = st.date_input("End Date", value=datetime(2023, 1, 31))

# Create two time input widgets for start and end times
start_time = st.time_input("Start Time", value=dt_time(0, 0))
end_time = st.time_input("End Time", value=dt_time(23, 59))

# Combine date and time into datetime objects
start_datetime = datetime.combine(start_date, start_time)
end_datetime = datetime.combine(end_date, end_time)

# You can add a check to ensure the start date is not after the end date
if start_time > end_time:
    st.error("Error: End date must fall after start date.")

# Display the selected date range
st.write(f"Selected date range: {start_time.strftime('%Y-%m-%d')} to {end_time.strftime('%Y-%m-%d')}")

train_filter = st.selectbox("Select the Train id", list(range(102, 198)))
# dashboard title

st.title("Streaming SNCB Dashboard 🚆")

# top-level filters

# creating a single-element container.
placeholder = st.empty()

# dataframe filter
# Define the query with placeholders for time frame parameters
query_time_frame = f"""
SELECT *
FROM vehicle_data
WHERE timestamps_UTC BETWEEN '{start_datetime}' AND '{end_datetime}'
AND mapped_veh_id = '{train_filter}'
ORDER BY timestamps_UTC ASC;
"""

# Execute the query and store the results in a DataFrame
df = pd.read_sql_query(query_time_frame, engine)

# near real-time / live feed simulation
live_df = pd.DataFrame(columns=df.columns)
# Initialize a DataFrame to keep track of boundary crossings
boundary_log_df = pd.DataFrame(columns=['timestamp', 'sensor', 'value', 'duration', 'boundary'])
boundary_log_df_full = pd.DataFrame(columns=['timestamp', 'sensor', 'value', 'boundary', 'lat', 'lon'])

# Initialize a DataFrame to keep track of boundary crossings
boundary_log_df = pd.DataFrame(columns=['start_timestamp', 'sensor', 'value', 'duration', 'boundary'])

# Dictionary to track if a sensor is currently above its boundary
boundary_status = {sensor: {'crossed': False, 'start_time': None} for sensor in ['rs_e_inairtemp_pc1', 'rs_e_inairtemp_pc2',
                                                                                 'rs_e_wattemp_pc1', 'rs_e_wattemp_pc2',
                                                                                 'rs_e_oilpress_pc1', 'rs_e_oilpress_pc2']}

# Boundary checks:
 # Check if any sensor value exceeds its boundary and log the incident
sensor_boundaries = {'rs_e_inairtemp_pc1': 65, 'rs_e_inairtemp_pc2': 65,
                         'rs_e_wattemp_pc1': 100, 'rs_e_wattemp_pc2': 100,
                         'rs_e_oilpress_pc1': 115, 'rs_e_oilpress_pc2': 115}

for index, row in df.iterrows():
    # add row to the current df
    live_df = pd.concat([live_df, pd.DataFrame([row])], ignore_index=True)

    # creating KPIs
    air_1 = live_df['rs_e_inairtemp_pc1'].iloc[-1]
    air_2 = live_df['rs_e_inairtemp_pc2'].iloc[-1]
    water_1 = live_df['rs_e_wattemp_pc1'].iloc[-1]
    water_2 = live_df['rs_e_wattemp_pc2'].iloc[-1]
    oil_1 = live_df['rs_e_oilpress_pc1'].iloc[-1]
    oil_2 = live_df['rs_e_oilpress_pc2'].iloc[-1]

    # Boundary checks:

    current_time = row['timestamps_utc']  # Replace with your actual timestamp column

    for sensor, boundary in sensor_boundaries.items():
        sensor_value = row[sensor]
        if sensor_value > boundary:
            boundary_log_df_full.append({
                    'start_timestamp': current_time,
                    'sensor': sensor,
                    'value': sensor_value,
                    'duration': 0,  # Initialize duration to 0
                    'boundary': boundary,
                    'lat': live_df['lat'].iloc[-1],
                    'lon': live_df['lon'].iloc[-1]
                }, ignore_index=True)
            if not boundary_status[sensor]['crossed']:
                # Sensor has just crossed the boundary
                boundary_status[sensor]['crossed'] = True
                boundary_status[sensor]['start_time'] = current_time
                boundary_log_df = boundary_log_df.append({
                    'start_timestamp': current_time,
                    'sensor': sensor,
                    'value': sensor_value,
                    'duration': 0,  # Initialize duration to 0
                    'boundary': boundary
                }, ignore_index=True)
            else:
                # Update the duration in minutes
                duration_minutes = (current_time - boundary_status[sensor]['start_time']).total_seconds() / 60
                boundary_log_df.at[
                    boundary_log_df[boundary_log_df['sensor'] == sensor].index[-1], 'duration'] = duration_minutes
        else:
            # Sensor value has gone below the boundary
            boundary_status[sensor]['crossed'] = False
            boundary_status[sensor]['start_time'] = None

    with placeholder.container():
        # Assuming live_df['timestamps_utc'].iloc[-1] is a datetime object
        time_value = live_df['timestamps_utc'].iloc[-1]
        formatted_time = time_value.strftime("%A, %d %B %Y %H:%M:%S")
        relative_time = humanize.naturaltime(datetime.now() - time_value)

        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric(label="Air Temperature", value=f"{round(air_1)}°C")
        kpi2.metric(label="Water Temperature", value=f"{round(water_1)}°C")
        kpi3.metric(label="Oil Temperature", value=f"{round(oil_1)}°C")
        kpi4.metric(label="Time", value=formatted_time, delta=relative_time)

        # create two columns for charts

        fig_col1, fig_col2, fig_col3 = st.columns(3)

        with fig_col1:
            st.markdown("### Air Temperature Over Time")
            # Plotting air temperature from both sensors on the same graph
            fig_air = px.line(live_df, x='timestamps_utc', y=['rs_e_inairtemp_pc1', 'rs_e_inairtemp_pc2'],
                              labels={'value': 'Temperature (°C)', 'variable': 'Sensor'},
                              title='Air Temperature Over Time')
            fig_air.update_layout(legend_title_text='Sensor', xaxis_title='Time', yaxis_title='Air Temperature (°C)')
            # Adding maximum acceptable temperature line for air
            fig_air.add_hline(y=65, line_dash="dot", line_color="red", annotation_text="Max Acceptable Temp",
                              annotation_position="bottom right")
            st.plotly_chart(fig_air)

        with fig_col2:
            st.markdown("### Water Temperature Over Time")
            # Plotting water temperature from both sensors on the same graph
            fig_water = px.line(live_df, x='timestamps_utc', y=['rs_e_wattemp_pc1', 'rs_e_wattemp_pc2'],
                                labels={'value': 'Water Temperature (°C)', 'variable': 'Sensor'},
                                title='Water Temperature Over Time')
            fig_water.update_layout(legend_title_text='Sensor', xaxis_title='Time',
                                    yaxis_title='Water Temperature (°C)')
            # Adding maximum acceptable temperature line for water
            fig_water.add_hline(y=100, line_dash="dot", line_color="red", annotation_text="Max Acceptable Temp",
                                annotation_position="bottom right")
            st.plotly_chart(fig_water)

        with fig_col3:
            st.markdown("### Oil Pressure Over Time")
            # Plotting oil pressure from both sensors on the same graph
            fig_oil = px.line(live_df, x='timestamps_utc', y=['rs_e_oilpress_pc1', 'rs_e_oilpress_pc2'],
                              labels={'value': 'Oil Pressure', 'variable': 'Sensor'},
                              title='Oil Pressure Over Time')
            fig_oil.update_layout(legend_title_text='Sensor', xaxis_title='Time', yaxis_title='Oil Pressure')
            # Adding maximum acceptable temperature line for oil
            fig_oil.add_hline(y=115, line_dash="dot", line_color="red", annotation_text="Max Acceptable Temp",
                              annotation_position="bottom right")
            st.plotly_chart(fig_oil)

        fig_col1_r2, fig_col2_r2, fig_col3_r2 = st.columns(3)
        with fig_col1_r2:
            st.markdown("### Location")

            # Select the last three entries of the live DataFrame
            last_entries = live_df.tail(3)

            # Check if there are enough entries
            if len(last_entries) >= 3:
                # Create a map with the last three points and connect them with a line
                map_fig = px.line_mapbox(
                    last_entries, lat='lat', lon='lon',
                    zoom=12, height=300,
                    color_discrete_sequence=["red"]  # Set the line color to red
                )

                # Add scatter points to the map for better visibility
                map_fig.add_scattermapbox(
                    lon=last_entries['lon'],
                    lat=last_entries['lat'],
                    mode='markers',
                    marker=dict(size=30, color='blue'),  # Change size and color as needed
                )

                # Update the layout of the map
                map_fig.update_layout(mapbox_style="open-street-map")
                map_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

                # Display the map in Streamlit
                st.plotly_chart(map_fig)
            else:
                st.write("Not enough location data available for plotting.")

        with fig_col2_r2:
            st.markdown("### Boundary crossings:")
            st.dataframe(boundary_log_df)
        time.sleep(0.1)

        with fig_col3_r2:
            st.markdown("### Anomaly Heatmap")

            # Check if there are enough entries
            if not boundary_log_df.empty:
                # Create a base map
                m = folium.Map(location=[50.8503, 4.3517], zoom_start=10)  # Set default location

                # Create a heatmap
                heatmap_data = boundary_log_df_full[
                    ['lat', 'lon']].values.tolist()  # Replace with your lat-long columns
                HeatMap(heatmap_data).add_to(m)

                # Render the map with Streamlit Folium component
                folium_static(m)
            else:
                st.write("No anomaly data available for heatmap.")
    # placeholder.empty()