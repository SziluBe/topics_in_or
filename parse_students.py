import pandas as pd
import numpy as np

# Load the data into a pandas table
df = pd.read_excel("Anon Enrollment Data.xlsx")

print(df)
print(df.columns)

# create dictionary with keys being UUN's from column "UUN" and
# values being lists of courses from column "Course Code"
# found in the same row
uuns = df['UUN'].unique()
uuns = {uuns[i]: set() for i in range(len(uuns))}
for index, row in df.iterrows():
    uun = row['UUN']
    course = row['Course Code']
    uuns[uun].add(course)

print(uuns)

