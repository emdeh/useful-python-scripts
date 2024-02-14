import pandas as pd
import os
import csv
import fitz  # PyMuPDF
from dotenv import load_dotenv

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load the environment variables
load_dotenv()

# List of folders to process
folders = [
    os.getenv('FOLDER_PATH_1', ''),
    os.getenv('FOLDER_PATH_2', ''),
    os.getenv('FOLDER_PATH_3', ''),
    os.getenv('FOLDER_PATH_4', '')
]

# Path for the output CSV file
output_csv_path = os.getenv('OUTPUT_PATH')

# Count the number of pages in a single PDF
def count_pdf_pages(pdf_path):
    try:
        with fitz.open(pdf_path) as doc:
            return len(doc)
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return 0

def process_folders(folders):
    # Lists to store data for each sheet
    detailed_data = []
    summary_data = []

    grand_total_docs = 0
    grand_total_pages = 0

    for folder in folders:
        total_pdfs = 0
        total_pages = 0
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.lower().endswith('.pdf'):
                    pdf_path = os.path.join(root, file)
                    pages = count_pdf_pages(pdf_path)
                    total_pdfs += 1
                    total_pages += pages
                    detailed_data.append([folder, file, pages])
        summary_data.append([folder, total_pdfs, total_pages])
        grand_total_docs += total_pdfs
        grand_total_pages += total_pages

    # Append grand totals to summary_data
    summary_data.append(['Grand Total', grand_total_docs, grand_total_pages])

    return detailed_data, summary_data

# Process folders and get data for sheets
detailed_data, summary_data = process_folders(folders)

# Convert lists to DataFrames
detailed_df = pd.DataFrame(detailed_data, columns=['Folder', 'Document Name', 'Total Pages'])
summary_df = pd.DataFrame(summary_data, columns=['Folder', 'Number of Documents', 'Total Pages'])

# Save to Excel with two sheets
with pd.ExcelWriter(output_csv_path, engine='openpyxl') as writer:
    detailed_df.to_excel(writer, sheet_name='Pages Per Document', index=False)
    summary_df.to_excel(writer, sheet_name='Summary', index=False)
