import pandas as pd
import xml.etree.ElementTree as ET


def main():
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
        if "MATH" in course:
            uuns[uun].add(course)

    print(uuns)

    # create a new xml tree
    root = ET.Element("students")

    # add a student element for each UUN
    for uun in uuns:
        student = ET.SubElement(root, "student", id=uun)
        for course in uuns[uun]:
            ET.SubElement(student, "course", id=course)

    # write the tree to a file
    # with open("students.xml", "wb") as f:
    #     f.write(ET.tostring(root))

    return root

