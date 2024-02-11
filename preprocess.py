import pandas as pd

# Specify the file path
file_path = "School of Mathematics - Timetable Data.xlsx"

# Load the data into a pandas table
df = pd.read_excel(file_path)

# Print the table
print(df)

# Print the column names
print(df.columns)
