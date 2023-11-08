import csv
from datetime import datetime

def time_diff_seconds(start, end):
    fmt = '%Y-%m-%d %H:%M:%S'
    tdelta = datetime.strptime(end, fmt) - datetime.strptime(start, fmt)
    return tdelta.total_seconds()

def segment_continuous_data(csv_input_filename, jump_threshold=60):
    segments = []
    current_segment = []

    with open(csv_input_filename, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        prev_timestamp = None

        for row in reader:
            if prev_timestamp is not None:
                diff = time_diff_seconds(prev_timestamp, row['timestamps_UTC'])

                if diff > jump_threshold:
                    # If time jump is greater than the threshold, start a new segment
                    if current_segment:
                        segments.append(current_segment)
                    current_segment = []

            current_segment.append(row)
            prev_timestamp = row['timestamps_UTC']

        # Append the last segment if it exists
        if current_segment:
            segments.append(current_segment)

    # Now write each segment to a new CSV file
    for i, segment in enumerate(segments):
        segment_filename = f'segment_{i+1}.csv'
        with open(segment_filename, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=reader.fieldnames, delimiter=';')
            writer.writeheader()
            for row in segment:
                writer.writerow(row)

        print(f'Continuous segment {i+1} written to {segment_filename} with {len(segment)} entries.')

    return len(segments)

# Example usage:
csv_file = 'mapped_veh_id_102.0.csv'  # Replace with your CSV filename
num_segments = segment_continuous_data(csv_file, jump_threshold=600)  # 600 seconds as a jump threshold, 10 minutes
print(f'Total segments created: {num_segments}')
