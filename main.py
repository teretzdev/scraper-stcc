import re
import fitz  # PyMuPDF for reading the PDF
import pandas as pd

def extract_transform_data_robust(page_text):
    entries = []
    lines = page_text.split('\n')
    pattern_date = r'\d{2}/\d{2}/\d{2}'

    i = 0
    while i < len(lines):
        if re.match(pattern_date, lines[i]):
            book_date = lines[i].strip()
            name = lines[i + 1].strip() if i + 1 < len(lines) else ''
            address = lines[i + 2].strip() if i + 2 < len(lines) else ''
            city_state_zip = lines[i + 3].strip() if i + 3 < len(lines) else ''
            charge = lines[i + 4].strip() if i + 4 < len(lines) else ''
            release_info = lines[i + 5].strip().split() if i + 5 < len(lines) else []

            release_date = release_info[0] if len(release_info) > 1 else 'Unknown'
            days = release_info[-1] if len(release_info) > 2 else 'Unknown'

            last_name, first_name = name.split(' ', 1) if ' ' in name else (name, '')
            city, state_zip = city_state_zip.rsplit(' ', 1) if ' ' in city_state_zip else (city_state_zip, '')
            state, zip_code = state_zip.split(' ', 1) if ' ' in state_zip else (state_zip, '')

            entry = {
                'LastName': last_name,
                'FirstName': first_name,
                'Address': address,
                'City': city,
                'State': state,
                'Zip': zip_code,
                'Charge': charge,
                'BookDate': book_date,
                'ReleaseDate': release_date,
                'Days': days
            }
            entries.append(entry)

            i += 6  # Skip lines to move to the next record
        else:
            i += 1  # Move to the next line if the current line doesn't match the date pattern

    return entries

def process_pdf_to_excel(pdf_file_path, extraction_function):
    all_entries = []

    with fitz.open(pdf_file_path) as doc:
        for page in doc:
            page_text = page.get_text()
            if page_text:
                page_entries = extraction_function(page_text)
                all_entries.extend(page_entries)

    if not all_entries:
        print("Error: No data extracted from the PDF file.")
        return None

    # Create a DataFrame from the extracted data
    df = pd.DataFrame(all_entries)

    # Specify the output Excel file path
    excel_output_path = './InmateRecords.xlsx'

    # Save the DataFrame to an Excel file
    df.to_excel(excel_output_path, index=False)

    return excel_output_path

# Process the PDF and generate an Excel file
pdf_file_path = './stcc_raw_data.pdf'
output_excel_path = process_pdf_to_excel(pdf_file_path, extract_transform_data_robust)

if output_excel_path:
    print(f"Excel file generated successfully: {output_excel_path}")
