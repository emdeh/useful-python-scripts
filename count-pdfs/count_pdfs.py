import os
import csv
import fitz  # PyMuPDF

def count_pdf_pages(pdf_path):
    """Counts the number of pages in a single PDF."""
    try:
        with fitz.open(pdf_path) as doc:
            return len(doc)
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return 0

def process_folder(folder_path):
    """Processes a single folder for PDFs and their pages."""
    results = []
    total_pdfs = 0
    total_pages = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.pdf'):
                total_pdfs += 1
                pdf_path = os.path.join(root, file)
                pages = count_pdf_pages(pdf_path)
                total_pages += pages
                results.append((file, pages))
    return total_pdfs, total_pages, results

def write_results_to_csv(folders, output_csv_path):
    """Writes the processing results of multiple folders to a CSV file."""
    grand_total_pdfs = 0
    grand_total_pages = 0
    with open(output_csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Folder', 'PDF File', 'Number of Pages'])
        for folder in folders:
            total_pdfs, total_pages, results = process_folder(folder)
            grand_total_pdfs += total_pdfs
            grand_total_pages += total_pages
            for file, pages in results:
                writer.writerow([folder, file, pages])
            writer.writerow(['Total in Folder', total_pdfs, total_pages])
        writer.writerow(['Grand Total', grand_total_pdfs, grand_total_pages])

# List of folders to process
folders = [
    'folder_path_1',
    'folder_path_2',
    'folder_path_3',
    'folder_path_4'
]

# Path for the output CSV file
output_csv_path = 'pdf_summary.csv'

# Process the folders and write the results
write_results_to_csv(folders, output_csv_path)
