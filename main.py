import re
import pandas as pd

def expand_year(cr_no):
   
    match = re.search(r'/(\d{2})$', cr_no)
    if match:
        year = int(match.group(1))
        full_year = 1900 + year if year >= 50 else 2000 + year
        return re.sub(r'/\d{2}$', f'/{full_year}', cr_no)
    return cr_no

def parse_crime_data_robust(lines):
    processed_data = []
    unmatched_lines = []
    
    separators = [r"u/s[.:]?", r"us\.", r"u/s-", r"sec", r"us"] 
    pattern_text = r"^(.*?)\s*(?:" + "|".join(separators) + r")\s*(.*)$"
    pattern = re.compile(pattern_text, re.IGNORECASE)

    for line in lines:
        line = str(line).strip().replace('\n', ' ')
        if not line or line.startswith("[source"):
            continue

        match = pattern.search(line)
        if match:
            cr_no = match.group(1).strip()
            section = match.group(2).strip()

            
            cleaned_cr_no = re.sub(r'[^0-9/]', '', cr_no)
            cleaned_cr_no = expand_year(cleaned_cr_no)

            processed_data.append({
                "Original_Text": line,
                "Cr_No": cleaned_cr_no,
                "Section": section
            })
        else:
            unmatched_lines.append(line)
            processed_data.append({
                "Original_Text": line,
                "Cr_No": "INCORRECT",
                "Section": "INCORRECT"
            })
            
    return processed_data, unmatched_lines



input_excel_file = '/Users/midhun/Developer/Git/Tuty_XLSX_Formater/Data/Remand Accused Details (1)-1.xlsx'
output_excel_file = '/Users/midhun/Developer/Git/Tuty_XLSX_Formater/Output/Cleaned.xlsx' 
column_to_process = 'Cr_no & Section'

try:
    df_input = pd.read_excel(input_excel_file)
    print(f"Successfully loaded data from '{input_excel_file}'")

    if column_to_process not in df_input.columns:
        print(f"Error: Column '{column_to_process}' not found in the Excel file.")
    else:
        lines_to_process = df_input[column_to_process].astype(str).tolist()
        processed_data, unmatched_lines = parse_crime_data_robust(lines_to_process)

        df_output = pd.DataFrame(processed_data)
        df_output.to_excel(output_excel_file, index=False, engine='openpyxl')
        print(f"Successfully processed the data and saved it to '{output_excel_file}'")

        if unmatched_lines:
            print("\nWarning: The following original lines could not be parsed (Cr_No and Section set to '-'):")
            for line in unmatched_lines:
                print(f"- {line}")

except FileNotFoundError:
    print(f"Error: The input file '{input_excel_file}' was not found.")
    print("Please make sure the file path is correct and the file exists.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")



    