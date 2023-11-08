# This function filters the data on a certain attribute
# For example it can filter the data to all entries with a mapped_veh_id = 181
import csv
import os
from tqdm import tqdm

def filter_data_by_attribute(csv_input_filename, csv_output_filename, filter_attribute, filter_value):
    """
    Filters a CSV file to include only rows with a specified attribute value and writes it to a new CSV file.

    Parameters:
    csv_input_filename (str): The path to the input CSV file.
    csv_output_filename (str): The path to the output CSV file.
    filter_attribute (str): The attribute to filter by.
    filter_value (str): The value of the attribute to filter by.
    """

    with open(csv_input_filename, mode='r', newline='', encoding='utf-8') as csvfile, \
            open(csv_output_filename, mode='w', newline='', encoding='utf-8') as outputfile:

        reader = csv.DictReader(csvfile, delimiter=';')
        writer = csv.DictWriter(outputfile, fieldnames=reader.fieldnames, delimiter=';')

        # Write the header to the output file
        writer.writeheader()

        # Iterate over each row and write rows with the specified attribute value
        for row in reader:
            if row[filter_attribute] == filter_value:
                writer.writerow(row)

def split_csv_by_unique_attributes(csv_input_filename, attribute, output_folder):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    file_handles = {}
    writers = {}

    # Determine the number of rows (for the progress bar)
    with open(csv_input_filename, mode='r', newline='', encoding='utf-8') as csvfile:
        total_rows = sum(1 for row in csvfile) - 1  # Subtract one for the header

    # Process the CSV file
    with open(csv_input_filename, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        progress_bar = tqdm(total=total_rows, unit='row')

        for row in reader:
            progress_bar.update(1)  # Update the progress bar by one row
            key = row[attribute]
            # Create a new file and writer if we haven't seen this attribute value yet
            if key not in writers:
                output_filename = f"{attribute}_{key}.csv".replace('/', '_').replace('\\', '_').replace(' ',
                                                                                                        '_').replace(
                    ':', '_')
                output_path = os.path.join(output_folder, output_filename)
                file_handles[key] = open(output_path, mode='w', newline='', encoding='utf-8')
                writers[key] = csv.DictWriter(file_handles[key], fieldnames=reader.fieldnames, delimiter=';')
                writers[key].writeheader()

            writers[key].writerow(row)

        progress_bar.close()  # Close the progress bar

    # Close all file handles
    for file_handle in file_handles.values():
        file_handle.close()


# Example usage:
csv_input_filename = 'ar41_for_ulb.csv'  # Replace with your CSV file path
attribute_to_split_by = 'mapped_veh_id'  # Replace with the attribute you want to split by
output_folder = 'split_csv_files'  # Replace with your desired output folder name

# This will create a new folder 'split_csv_files' in the current directory and save the split CSV files there
split_csv_by_unique_attributes(csv_input_filename, attribute_to_split_by, output_folder)