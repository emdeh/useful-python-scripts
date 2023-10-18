'''
Created this script because I was having trouble with the output of https://github.com/raviqqe/muffet (the Windows version specifically).
This script takes a JSON output file from muffet and converts it into CSV.
example:
  Open a cmd line
  Run muffet as you need like 'muffet.exe https://www.mysite.come /follow-robots-txt /max-connections:200 /format:json /v > results.json
  Wait for it to finish
  Then, in the same dir, run: json_to_csv.py results.json
'''
import sys
import json
import csv

if len(sys.argv) != 2:
    print("Usage: python json_to_csv.py <input_json_file>")
    sys.exit(1)

input_json_file = sys.argv[1]

try:
    with open(input_json_file, 'r') as json_file:
        data = json.load(json_file)

    csv_file = input_json_file.replace('.json', '_converted.csv')

    with open(csv_file, 'w', newline='') as csv_file:
        header = set(['Page'])  # Initialize the set with the new 'Page' field
        for item in data:
            for link in item.get('links', []):
                properties = link.keys()
                header.update(properties)

        column_order = ['Page', 'url', 'status', 'error'] + sorted(header - {'Page', 'url', 'status', 'error'})

        csv_writer = csv.DictWriter(csv_file, fieldnames=column_order)
        csv_writer.writeheader()

        for item in data:
            top_level_url = item.get('url', 'Unknown')  # Get the top-level URL
            for link in item.get('links', []):
                if not link.get('status'):
                    link['status'] = 'no status - check error column for more info'
                
                # Assign the top-level URL to the 'Page' field
                link['Page'] = top_level_url
                
                csv_writer.writerow(link)

    print(f"Conversion completed. CSV file saved as {csv_file}")

except FileNotFoundError:
    print(f"Error: The specified input JSON file '{input_json_file}' was not found.")
except Exception as e:
    print(f"An error occurred: {str(e)}")
