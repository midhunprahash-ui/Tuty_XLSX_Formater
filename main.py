import pandas as pd
import re

df = pd.read_excel('/Users/midhun/Developer/Tuty_Project/Remand Accused Details (1)-1.xlsx')


def split_cr_section(text):
    if pd.isna(text):  
        return pd.Series([None, None])
    
    # Normalize all variations of 'u/s' to 'u/s'
    normalized_text = re.sub(r'u/s', 'u/s', text, flags=re.IGNORECASE)
    
    # Now split by the normalized 'u/s'
    parts = normalized_text.split('u/s')
    
    cr_no_raw = parts[0]
    # Keep only digits and '/'
    cr_no = re.sub(r'[^0-9/]', '', cr_no_raw)
    
    section = parts[1] if len(parts) > 1 else ""
    return pd.Series([cr_no, section])

df[['Cr.No', 'Section']] = df['Cr_no & Section'].apply(split_cr_section)

# Save to Excel
df.to_excel('/Users/midhun/Developer/Tuty_Project/Remand_Accused_Details_Processed.xlsx', index=False)

print("File saved successfully!")
