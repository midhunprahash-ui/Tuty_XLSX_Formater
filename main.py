import pandas as pd
import re


input_file_path = '/Users/midhun/Developer/Git/Tuty_XLSX_Formater/Data/Remand Accused Details (1)-1.xlsx'
output_file_path = '/Users/midhun/Developer/Git/Tuty_XLSX_Formater/Output/Processed.xlsx'


df = pd.read_excel(input_file_path)


pattern_to_normalize_us = re.compile(r"^(.*?)\s*(?:u/s[.:]?|u/s-|us\.|U/S)\s*(.*)$", re.IGNORECASE)


if not df['Cr_no & Section'].astype(str).str.contains(pattern_to_normalize_us, na=False).any():
    print("Check the Cr.No and Section - No variations of 'us' or 'u/s' found in the entire column.")
else:
    def split_cr_section(text):
        
        if pd.isna(text):
            return pd.Series([None, None])

        
        processed_text = str(text)

        
        processed_text = pattern_to_normalize_us.sub('u/s', processed_text)

       
        parts = processed_text.split('u/s')

       
        cr_no_raw = parts[0].strip()
        cr_no = re.sub(r'[^0-9/]', '', cr_no_raw)

        
        section = parts[1].strip() if len(parts) > 1 else ""
        section = section.strip('/') 
        return pd.Series([cr_no, section])

   
    df[['Cr.No', 'Section']] = df['Cr_no & Section'].apply(split_cr_section)

    
    df.to_excel(output_file_path, index=False)
    print("File saved successfully!")