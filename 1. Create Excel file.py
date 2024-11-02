import pandas as pd

# Define the data
data = [['Gosia', 18], ['Eryka', 31], ['Ola', 25]]
Example1 = pd.DataFrame(data, columns=['Name', 'Age'])

# Define the file path
file_path = r'C:\Users\plmala\OneDrive - Coloplast A S\Desktop\Python\Internal Trainers\Example1.xlsx'

# Save the DataFrame to an Excel file
Example1.to_excel(file_path, index=False)

print(f'Excel file saved at: {file_path}')
