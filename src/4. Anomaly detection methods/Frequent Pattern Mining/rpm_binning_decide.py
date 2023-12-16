# Assuming that you have already established a connection to the database using SQLAlchemy as shown previously
# and that you have a table named 'vehicle_data' which contains RPM data in columns 'rs_e_rpm_pc1' and 'rs_e_rpm_pc2'.

# Let's first write the code to fetch the RPM data from the database.
from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt

# Database connection parameters
dbname = 'DataMining'
user = 'postgres'
password = 'datamining'
host = 'localhost'
port = '5433'

# Establish a connection to the database
engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{dbname}')

# Define the query to select RPM columns
query = """
SELECT rs_e_rpm_pc1, rs_e_rpm_pc2
FROM vehicle_data;
"""

# Execute the query and fetch the data into a DataFrame
df_rpm = pd.read_sql_query(query, engine)

# Close the database connection
engine.dispose()

# Calculate summary statistics for the RPM columns
rpm_stats_pc1 = df_rpm['rs_e_rpm_pc1'].describe()
rpm_stats_pc2 = df_rpm['rs_e_rpm_pc2'].describe()

print("Summary Statistics for RS_E_RPM_PC1:")
print(rpm_stats_pc1)
print("\nSummary Statistics for RS_E_RPM_PC2:")
print(rpm_stats_pc2)

# Plot histograms for the RPM columns to visualize the distribution
fig, ax = plt.subplots(1, 2, figsize=(14, 6))

# Histogram for RS_E_RPM_PC1
ax[0].hist(df_rpm['rs_e_rpm_pc1'].dropna(), bins=20, color='skyblue', edgecolor='black')
ax[0].set_title('Histogram of RS_E_RPM_PC1')
ax[0].set_xlabel('RPM')
ax[0].set_ylabel('Frequency')

# Histogram for RS_E_RPM_PC2
ax[1].hist(df_rpm['rs_e_rpm_pc2'].dropna(), bins=20, color='salmon', edgecolor='black')
ax[1].set_title('Histogram of RS_E_RPM_PC2')
ax[1].set_xlabel('RPM')
ax[1].set_ylabel('Frequency')

plt.tight_layout()
plt.show()
