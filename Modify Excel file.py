import pandas as pd
from datetime import datetime

# Path
original_file_path = r'C:\Users\plmala\OneDrive - Coloplast A S\Desktop\Python\PPM\Hello\Spend by categories, suppliers, companies.xlsx'

# Load the data
df = pd.read_excel(original_file_path)

# Filter
df = df[df['Coloplast Year GL'] == '23/24']

# Delete
df = df[df['12 Month Rolling GL'] != 'OTHER']

# Date format
timestamp = datetime.now().strftime("%d.%m.%Y")
new_file_path = original_file_path.replace('.xlsx', f'_{timestamp}.xlsx')

# Save
df.to_excel(new_file_path, index=False)

print(f"The file has been modified and saved as: {new_file_path}")