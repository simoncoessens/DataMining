import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv(r"ar41_for_ulb.csv", delimiter=';')

# Data Preprocessing
# Assuming 'timestamps_UTC' is the timestamp column
data['timestamps_UTC'] = pd.to_datetime(data['timestamps_UTC'])
data = data.sort_values(by='timestamps_UTC')

# EDA: Visualize the Data
# Plot temperature time series for PC1 and PC2
plt.figure(figsize=(12, 6))
plt.plot(data['timestamps_UTC'], data['RS_E_InAirTemp_PC1'], label='InAirTemp_PC1', color='blue')
plt.plot(data['timestamps_UTC'], data['RS_E_InAirTemp_PC2'], label='InAirTemp_PC2', color='green')
plt.xlabel('Timestamp')
plt.ylabel('Temperature (°C)')
plt.title('Temperature Time Series for PC1 and PC2')
plt.legend()
plt.show()

# Plot pressure time series for PC1 and PC2
plt.figure(figsize=(12, 6))
plt.plot(data['timestamps_UTC'], data['RS_E_OilPress_PC1'], label='OilPress_PC1', color='blue')
plt.plot(data['timestamps_UTC'], data['RS_E_OilPress_PC2'], label='OilPress_PC2', color='green')
plt.xlabel('Timestamp')
plt.ylabel('Pressure (kPa)')
plt.title('Pressure Time Series for PC1 and PC2')
plt.legend()
plt.show()

# Plot RPM time series for PC1 and PC2
plt.figure(figsize=(12, 6))
plt.plot(data['timestamps_UTC'], data['RS_E_RPM_PC1'], label='RPM_PC1', color='blue')
plt.plot(data['timestamps_UTC'], data['RS_E_RPM_PC2'], label='RPM_PC2', color='green')
plt.xlabel('Timestamp')
plt.ylabel('RPM')
plt.title('RPM Time Series for PC1 and PC2')
plt.legend()
plt.show()

# Scatter plot of GPS coordinates
plt.figure(figsize=(10, 6))
plt.scatter(data['lon'], data['lat'], c='b', marker='o', s=5, alpha=0.5)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Scatter Plot of GPS Coordinates')
plt.show()

# Additional EDA can include statistical summaries, histograms, and correlation analysis.

# Summary statistics
summary = data.describe()
print(summary)

# Histograms for temperature, pressure, and RPM
data[['RS_E_InAirTemp_PC1', 'RS_E_OilPress_PC1', 'RS_E_RPM_PC1']].hist(bins=20, figsize=(12, 6))
plt.suptitle('Histograms for Temperature, Pressure, and RPM for PC1')
plt.show()

# Correlation matrix
correlation_matrix = data.corr()
plt.figure(figsize=(10, 8))
plt.matshow(correlation_matrix, cmap='coolwarm', fignum=1)
plt.xticks(range(len(data.columns)), data.columns, rotation=90)
plt.yticks(range(len(data.columns)), data.columns)
plt.colorbar()
plt.title('Correlation Matrix')
plt.show()
