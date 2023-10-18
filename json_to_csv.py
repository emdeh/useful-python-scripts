import sys
import json
import csv

# Check if the correct number of arguments is provided
if len(sys.argv) != 2:
    print("Usage: python json_to_csv.py <input_json_file>")
    sys.exit(1)

# Get the input JSON file name from the command-line argument
input_json_file = sys.argv[1]

try:
    # Open the JSON file for reading
    with open(input_json_file, 'r') as json_file:
        data = json.load(json_file)

    # Create the CSV output file name
    csv_file = input_json_file.replace('.json', '_converted.csv')

    # Open the CSV file for writing
    with open(csv_file, 'w', newline='') as csv_file:
        # Get a list of all unique property names within the links
        header = set()
        for item in data:
            for link in item.get('links', []):
                properties = link.keys()
                header.update(properties)

        # Define the desired column order
        column_order = ['url', 'status', 'error'] + sorted(header - {'url', 'status', 'error'})

        # Create a CSV writer with the desired column order
        csv_writer = csv.DictWriter(csv_file, fieldnames=column_order)

        # Write the header row
        csv_writer.writeheader()

        # Iterate through each JSON object and its links
        for item in data:
            for link in item.get('links', []):
                # Check if 'status' is blank or doesn't exist, and handle accordingly
                if not link.get('status'):
                    link['status'] = 'no status - check error column for more info'
                
                # Write a row for each link with all available properties
                csv_writer.writerow(link)

    print(f"Conversion completed. CSV file saved as {csv_file}")

except FileNotFoundError:
    print(f"Error: The specified input JSON file '{input_json_file}' was not found.")

except Exception as e:
    print(f"An error occurred: {str(e)}")
