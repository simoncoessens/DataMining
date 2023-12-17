import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

# Database connection parameters
dbname = 'DataMining'
user = 'postgres'
password = 'datamining'
host = 'localhost'  # localhost or the server address
port = '5433'  # default PostgreSQL port is 5432

# Establish a connection to the database
connection_str = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
engine = create_engine(connection_str)

query = """
SELECT rs_e_inairtemp_pc1, 
       rs_e_inairtemp_pc2, 
       rs_e_wattemp_pc1, 
       rs_e_wattemp_pc2, 
       rs_t_oiltemp_pc1, 
       rs_t_oiltemp_pc2, 
       rs_e_rpm_pc1, 
       rs_e_rpm_pc2
FROM vehicle_data
LIMIT 5000000;
"""

# Execute the query and fetch the data into a DataFrame
df = pd.read_sql_query(query, engine)
print('data received')
# Close the database connection
engine.dispose()


# Define your bins
air_bins = [-float('inf'), 25, 45, 60, 65, float('inf')]
water_bins = [-float('inf'), 60, 80, 95, 100, float('inf')]
oil_bins = [-float('inf'), 80, 95, 110, 115, float('inf')]
rpm_bins = [0, 500, 790, 812, 1200, 3000]  # Upper limit set to 3000 as a placeholder

# Define labels for the bins
air_labels = ['<25°C', '25-45°C', '45-60°C', '60-65°C', '>=65°C']
water_labels = ['<60°C', '60-80°C', '80-95°C', '95-100°C', '>=100°C']
oil_labels = ['<80°C', '80-95°C', '95-110°C', '110-115°C', '>=115°C']
rpm_labels = ['Very Low RPM', 'Low RPM', 'Medium RPM', 'High RPM', 'Very High RPM']

# Bin the temperature and RPM columns
temp_columns = ['rs_e_inairtemp_pc1', 'rs_e_inairtemp_pc2', 'rs_e_wattemp_pc1', 'rs_e_wattemp_pc2', 'rs_t_oiltemp_pc1', 'rs_t_oiltemp_pc2']
rpm_columns = ['rs_e_rpm_pc1', 'rs_e_rpm_pc2']

for col in temp_columns:
    if 'inair' in col:
        df[col + '_bin'] = pd.cut(df[col], bins=air_bins, labels=air_labels, right=False)
    elif 'wattemp' in col:
        df[col + '_bin'] = pd.cut(df[col], bins=water_bins, labels=water_labels, right=False)
    elif 'oiltemp' in col:
        df[col + '_bin'] = pd.cut(df[col], bins=oil_bins, labels=oil_labels, right=False)

for col in rpm_columns:
    df[col + '_bin'] = pd.cut(df[col], bins=rpm_bins, labels=rpm_labels, right=False)


print('data binned')
# DATA EXPLORATION OF THE BINS:
# Example: Plotting the distribution of one of the binned columns
binned_columns = [col for col in df.columns if '_bin' in col]

for col in binned_columns:
    df[col].value_counts().plot(kind='bar')
    plt.title(f'Distribution of {col}')
    plt.ylabel('Count')
    plt.xlabel('Bins')
    plt.show()


# FREQUENT PATTERN MINING: APRIORI
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori

# Convert the DataFrame into a list of transactions, ensuring all items are strings
transactions = df[binned_columns].astype(str).values.tolist()

# Now apply the TransactionEncoder
te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
df_transactions = pd.DataFrame(te_ary, columns=te.columns_)

# Apply the Apriori algorithm to find frequent item sets
print('start apriori alg')
frequent_itemsets = apriori(df_transactions, min_support=0.1, use_colnames=True)  # Adjust min_support as needed

# Display frequent item sets
print(frequent_itemsets.sort_values(by='support', ascending=False))



