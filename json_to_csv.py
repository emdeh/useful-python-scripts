'''
Created this script because I was having trouble with the output of https://github.com/raviqqe/muffet (the Windows version specifically).
This script takes a JSON output file from muffet and converts it into two CSV files.
Example:
  Open a cmd line
  Run muffet as you need like 'muffet.exe https://www.mysite.com /follow-robots-txt /f /v /format:json > results.json
  Wait for it to finish
  Then, in the same dir, run: json_to_csv.py results.json
  The result will be two .csv files. One of just unique links found on the site, and the other links by page.
  The script will create and fill the Page column based on the top level object property of the JSON response.
  The url column will be each link that was checked.
  The status column will be the 200 code or will, if blank, refers to the error column for more information.
'''

import sys
import json
import csv
from collections import defaultdict

if len(sys.argv) != 2:
    print("Usage: python json_to_csv.py <input_json_file>")
    sys.exit(1)

input_json_file = sys.argv[1]

try:
    with open(input_json_file, 'r') as json_file:
        data = json.load(json_file)

    csv_file = input_json_file.replace('.json', '_converted.csv')
    unique_csv_file = input_json_file.replace('.json', '_unique_converted.csv')

    unique_links = {}
    header = set(['Page'])

    with open(csv_file, 'w', newline='') as csv_file:
        for item in data:
            for link in item.get('links', []):
                properties = link.keys()
                header.update(properties)

        column_order = ['Page', 'url', 'status', 'error'] + sorted(header - {'Page', 'url', 'status', 'error'})

        csv_writer = csv.DictWriter(csv_file, fieldnames=column_order)
        csv_writer.writeheader()

        for item in data:
            top_level_url = item.get('url', 'Unknown')
            for link in item.get('links', []):
                if not link.get('status'):
                    link['status'] = 'no status - check error column for more info'

                link['Page'] = top_level_url
                
                csv_writer.writerow(link)
                
                # Store unique links
                unique_links[link['url']] = link

    # Create unique links CSV
    with open(unique_csv_file, 'w', newline='') as unique_csv:
        unique_column_order = [col for col in column_order if col != 'Page']  # Remove 'Page' from unique CSV
        csv_writer = csv.DictWriter(unique_csv, fieldnames=unique_column_order)
        csv_writer.writeheader()
        
        for unique_link in unique_links.values():
            # Remove the 'Page' key-value pair before writing to unique CSV
            unique_link.pop('Page', None)
            csv_writer.writerow(unique_link)

    print(f"Conversion completed. CSV files saved as {csv_file} and {unique_csv_file}")

except FileNotFoundError:
    print(f"Error: The specified input JSON file '{input_json_file}' was not found.")
except Exception as e:
    print(f"An error occurred: {str(e)}")
