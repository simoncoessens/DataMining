import csv
import os
from datetime import datetime
from glob import glob
from tqdm import tqdm


def sort_csv_files_by_date(directory):
    # List all CSV files in the specified directory
    csv_files = glob(os.path.join(directory, '*.csv'))

    # Progress bar for the files
    for file_path in tqdm(csv_files, desc='Sorting Files'):
        # Read in all data from the CSV file
        with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            rows = list(tqdm(reader, desc=f'Reading {os.path.basename(file_path)}'))

        # Sort data by 'timestamps_UTC' column
        rows.sort(key=lambda x: datetime.strptime(x['timestamps_UTC'], '%Y-%m-%d %H:%M:%S'))

        # Write data back into the same CSV file, now sorted
        with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=reader.fieldnames, delimiter=';')
            writer.writeheader()
            # Progress bar for the rows
            for row in tqdm(rows, desc=f'Writing {os.path.basename(file_path)}'):
                writer.writerow(row)


# Example usage:
sort_csv_files_by_date('.')