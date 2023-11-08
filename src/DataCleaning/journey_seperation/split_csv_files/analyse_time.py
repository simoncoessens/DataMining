import csv
from datetime import datetime
import numpy as np

def analyze_time_jumps(csv_input_filename):
    # Helper function to calculate time difference in seconds
    def time_diff_seconds(start, end):
        fmt = '%Y-%m-%d %H:%M:%S'
        tdelta = datetime.strptime(end, fmt) - datetime.strptime(start, fmt)
        return tdelta.total_seconds()

    # Load data and calculate time differences
    time_jumps = []
    prev_timestamp = None

    with open(csv_input_filename, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            if prev_timestamp is not None:
                time_jumps.append(time_diff_seconds(prev_timestamp, row['timestamps_UTC']))
            prev_timestamp = row['timestamps_UTC']

    if not time_jumps:
        return "No data found or only one data point, unable to calculate time jumps."

    # Convert time jumps to a numpy array for statistical analysis
    time_jumps = np.array(time_jumps)

    # Perform statistical analysis
    stats = {
        'mean': np.mean(time_jumps),
        'median': np.median(time_jumps),
        'std_dev': np.std(time_jumps),
        'min': np.min(time_jumps),
        'max': np.max(time_jumps),
        '25th_percentile': np.percentile(time_jumps, 25),
        '75th_percentile': np.percentile(time_jumps, 75),
        'variance': np.var(time_jumps),
        'range': np.ptp(time_jumps)
    }

    return stats

# Example usage:
csv_file = 'mapped_veh_id_102.0.csv'  # Replace with your CSV filename
stats = analyze_time_jumps(csv_file)
print(stats)
