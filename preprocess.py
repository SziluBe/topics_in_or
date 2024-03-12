import pandas as pd
# elementTree for generating XML
import xml.etree.ElementTree as ET

# Specify the file path
file_path = "School of Mathematics - Timetable Data.xlsx"

# Load the data into a pandas table
df = pd.read_excel(file_path)

# Print the table
print(df)

# Print the column names
print(df.columns)

# create dictionary of id's and rooms names from column "Allocated Location Name"
room_ids = df['Allocated Location Name'].unique()
room_ids = {room_ids[i]: i for i in range(len(room_ids))}
print(room_ids)

# generate room constraints with capacities of and travel times between rooms; timeslots are 5 mins
room_capacities = {}
room_zones = {}

# delete contents of stuff.txt
open("eng_mat_1a.txt", "w").close()
open("credit_scoring.txt", "w").close()
open("lectures_with_slash.txt", "w").close()
open("non_lectures_with_slash.txt", "w").close()

# iterate over the rows of the dataframe
for index, row in df.iterrows():
    # get the room id and capacity
    room_name = row['Allocated Location Name']
    room_id = room_ids[room_name]
    occupancy = max(row['Planned Size'], row['Real Size'])
    zone = row['Zone Name']
    # add the room to the dictionary
    if room_id not in room_capacities or room_capacities[room_id] < occupancy:
        room_capacities[room_id] = occupancy
    room_zones[room_id] = zone
    if "Mathematics 1a" in row['Course Name']:
        with open("eng_mat_1a.txt", "a") as file:
            file.write(str(row["Activity"]) + "     |     " + str(row["Activity Type Name"]) + "     |     " + str(row["Teaching Week Pattern"]) + "     |     " + str(row["Scheduled Days"]) + "     |     " + str(row["Scheduled Start Time"]) + "     |     " + str(row["Scheduled End Time"]) + "     |     " + str(row["Allocated Location Name"]) + "\n")
    if "Credit Scoring" in row['Course Name']:
        with open("credit_scoring.txt", "a") as file:
            file.write(str(row["Activity"]) + "     |     " + str(row["Activity Type Name"]) + "     |     " + str(row["Teaching Week Pattern"]) + "     |     " + str(row["Scheduled Days"]) + "     |     " + str(row["Scheduled Start Time"]) + "     |     " + str(row["Scheduled End Time"]) + "     |     " + str(row["Allocated Location Name"]) + "\n")

print("#"*20)
print("ROOM CAPACITIES")
print(room_capacities)
print("#"*20)

# generate travel times between rooms
travel_times = {}

# Zones:
# JCMB
#   JCMB
#   *King's Buildings
#   Murchison House
#   *Central
#   Appleton Tower
#   40 George Square Lecture Theatres
#   Nucleus
# *King's Buildings
# Murchison House
# *Central
# Appleton Tower
# 40 George Square Lecture Theatres
# Nucleus

distances = {
    ("JCMB", "JCMB"): 0,
    ("JCMB", "*King's Buildings"): 2,
    ("JCMB", "Murchison House"): 3,
    ("JCMB", "*Central"): 9,
    ("JCMB", "Appleton Tower"): 9,
    ("JCMB", "40 George Square Lecture Theatres"): 9,
    ("JCMB", "Nucleus"): 1,
    ("*King's Buildings", "*King's Buildings"): 0,
    ("*King's Buildings", "Murchison House"): 2,
    ("*King's Buildings", "*Central"): 9,
    ("*King's Buildings", "Appleton Tower"): 9,
    ("*King's Buildings", "40 George Square Lecture Theatres"): 9,
    ("*King's Buildings", "Nucleus"): 9,
    ("Murchison House", "Murchison House"): 0,
    ("Murchison House", "*Central"): 9,
    ("Murchison House", "Appleton Tower"): 9,
    ("Murchison House", "40 George Square Lecture Theatres"): 9,
    ("Murchison House", "Nucleus"): 2,
    ("*Central", "*Central"): 0,
    ("*Central", "Appleton Tower"): 1,
    ("*Central", "40 George Square Lecture Theatres"): 1,
    ("*Central", "Nucleus"): 9,
    ("Appleton Tower", "Appleton Tower"): 0,
    ("Appleton Tower", "40 George Square Lecture Theatres"): 1,
    ("Appleton Tower", "Nucleus"): 9,
    ("40 George Square Lecture Theatres", "40 George Square Lecture Theatres"): 0,
    ("40 George Square Lecture Theatres", "Nucleus"): 9,
    ("Nucleus", "Nucleus"): 0
}

for room_id in room_ids.values():
    for room_id2 in room_ids.values():
        if room_id != room_id2:
            travel_times[(room_id, room_id2)] = [distances.get((room_zones[room_id], room_zones[room_id2]), distances.get((room_zones[room_id2], room_zones[room_id]), "nan")), room_zones[room_id], room_zones[room_id2]]

print("#"*20)
print("TRAVEL TIMES")
print(travel_times)
print("#"*20)

# (course) : (subpart, activity, weeks)
# TODO: find semester by "Delivery Semester" column for each course
# if empty, check if the course has any other activity with a delivery semester
# also check that all activities of a course have the same delivery semester
# also make sure to take into account the "Number of Teaching Weeks" column
# this can help us find two-semester courses
# for two-semester courses, we can add two courses to the dictionary,
# suffixing the course code with "A" and "B" for the first and second semester, respectively
courses = df['Course Code'].unique()

all_math_prefixed = True
for course in courses:
    if "MATH" not in course:
        all_math_prefixed = False
        break
print("All courses are prefixed with 'MATH':", all_math_prefixed)




#####
# Re-doing courses
#####

# Check if Activity - Scheduled Days pairs are unique
# Separate non-unique pairs into a separate dataframe
non_unique = df[df.duplicated(subset=['Activity', 'Scheduled Days'], keep=False)]
# non_unique = df[df.duplicated(subset=['Activity'], keep=False)]
print(non_unique)
# output non_unique to an excel file
non_unique.to_excel("non_unique.xlsx")

og_len = len(df)
print(len(df))

# Remove all duplicates from the dataframe (don't even keep the first occurrence)
df = df.drop_duplicates(subset=['Activity', 'Scheduled Days'], keep=False)
# df = df.drop_duplicates(subset=['Activity'], keep=False)
print("#"*20)

for index, row in df.iterrows():
    activity = row['Activity']
    days = row['Scheduled Days']
    if df[(df['Activity'] == activity) & (df['Scheduled Days'] == days)].shape[0] > 1:
    # if df[(df['Activity'] == activity)].shape[0] > 1:
        print(activity, days)

print(len(df))
print(len(non_unique))
assert len(df) + len(non_unique) == og_len
print("#"*20)

# Extract rows with both "/" and "Lecture" or "<" in Activity
weird_slash = df[((df['Activity'].str.contains("/")) & (df['Activity'].str.contains("Lecture"))) | (df['Activity'].str.contains("<")) | (df['Activity'].str.contains("Q&A")) | (df['Activity'].str.contains("Online"))]
print(weird_slash.columns)
print(weird_slash)

# output weird_lecture_slash to an excel file
weird_slash.to_excel("weird_slash.xlsx")

# Drop rows with both "/" and "Lecture" in Activity
df = df[~(((df['Activity'].str.contains("/")) & (df['Activity'].str.contains("Lecture"))) | (df['Activity'].str.contains("<")) | (df['Activity'].str.contains("Q&A")) | (df['Activity'].str.contains("Online")))]
print(len(df[((df['Activity'].str.contains("/")) & (df['Activity'].str.contains("Lecture"))) | (df['Activity'].str.contains("<")) | (df['Activity'].str.contains("Q&A")) | (df['Activity'].str.contains("Online"))]))
print(len(df))
print(len(non_unique))
print(len(weird_slash))
print(og_len)
assert len(df) + len(non_unique) + len(weird_slash) == og_len

# Make sure classes with a "/" are all in the same weeks
# If not, output them to a file
# If they are, just remove the "/" and keep the first part

copy_df = df.copy()
copy_df = copy_df[copy_df['Activity'].str.contains("/")]
copy_df['Activity'] = copy_df['Activity'].apply(lambda x: x.split("/")[0])

# Find unique Activity - Teaching Week Pattern pairs
unique_activity_weeks = copy_df[['Activity', 'Teaching Week Pattern']].drop_duplicates()

# bad_weeks_df = pd.DataFrame(columns=df.columns)

# for index, row in df.iterrows():
#     if "/" in row['Activity']:
#         weeks_str = row['Teaching Week Pattern']
#         for index2, row2 in df.iterrows():
#             if row2['Activity'] == row['Activity'] and row2['Teaching Week Pattern'] != weeks_str:
#                 bad_weeks_df = bad_weeks_df.append(row2)

print(unique_activity_weeks)

print(len(unique_activity_weeks['Activity'].unique()))

# Keep only non-unique Acticity rows
unique_activity_weeks = unique_activity_weeks[unique_activity_weeks.duplicated(subset=['Activity'], keep=False)]

print(unique_activity_weeks)
print(len(unique_activity_weeks))

# Get index column
index_col = unique_activity_weeks.index

# Get these indices from the original dataframe
bad_df = df.loc[index_col]

print(bad_df)

# output bad_df to an excel file
bad_df.to_excel("bad_weeks.xlsx")

# Remove these rows from the original dataframe
df = df.drop(index_col)

print(len(df))
print(len(non_unique))
print(len(weird_slash))
print(len(bad_df))
print(og_len)

assert len(df) + len(non_unique) + len(weird_slash) + len(bad_df) == og_len

print(df['Activity Type Name'].unique())

df.to_excel("cleaned.xlsx")

courses = {course: [] for course in courses}
subparts = {course: [] for course in courses}

for index, row in df.iterrows():
    course = row['Course Code']
    subpart = row['Activity Type Name'].split("/")[0]



quit()










courses = {course: [] for course in courses}
subparts = {course: [] for course in courses}

for index, row in df.iterrows():
    course = row['Course Code']
    subpart = row['Activity Type Name']
    activity_type = row['Activity Type Name']
    activity = row['Activity']
    weeks_str = row['Teaching Week Pattern']
    # split weeks_str on ', '
    weeks_split = weeks_str.split(', ')
    weeks = []
    # if any of the weeks is a range, expand it
    for i in range(len(weeks_split)):
        if '-' in weeks_split[i]:
            start, end = weeks_split[i].split('-')
            weeks.extend(range(int(start), int(end) + 1))
        else:
            weeks.append(int(weeks_split[i]))
    duration = row['Duration']
    # Convert duration from hours string (hh:mm) to multiples of 5 minutes
    duration = int(int(duration.split(':')[0]) * 12 + int(duration.split(':')[1]) / 5)
    day = row["Scheduled Days"]
    start = row["Scheduled Start Time"]
    parent = None
    for i in range(len(courses[course]), -1, -1):
        if "Lecture" in subpart:
            parent = i
            break
    # with open("asd.txt", "a") as file:
    if "/" in activity and ("Lecture" in subpart or "lecture" in subpart):
        # print(activity)
        # subpart = activity.split("/")[0]
        # file.write(activity + "\n")
        with open("lectures_with_slash.txt", "a") as file:
            file.write(activity + "\n")
        continue # TODO
    elif "/" in activity:
        # print(activity)
        subpart = activity.split("/")[0]
        with open("non_lectures_with_slash.txt", "a") as file:
            file.write(activity + "\n")
        # file.write(activity + "\n")
    else:
        subpart = activity
    penalties = ...
    courses[course].append((subpart, activity, weeks, duration))
    # if subpart not in subparts[course]:
    have_subpart = False
    for i in range(len(subparts[course])):
        if subpart == subparts[course][i][0]:
            have_subpart = True
            break
    if not have_subpart:
        subparts[course].append([subpart, activity_type])

for course in subparts:
    for i in range(len(subparts[course])):
        subparts[course][i][0] = str(i + 1) + "_" + subparts[course][i][0]

print("#"*20)
print("COURSES")
print(courses) #NOTE
print("#"*20)

# match rooms with possible activity types #TODO: this will probably require some manual work
rooms = {k: set() for k in room_ids.keys()}
activity_types_df = df['Activity Type Name'].unique()
activity_types = set()
for at in activity_types_df:
    activity_types.add(at)

print("#"*20)
print("ACTIVITY TYPES")
print(activity_types) #NOTE
print("#"*20)

# {'*Workshop', '*Lecture - Online Pre-recorded', 'Oral Presentation', '*Workshop - Online Live', 'Computer Workshop', 'Q&A Session', 'Self Study', 'Examples Class', '*Lecture', '*Lecture - Online Live'}
# groupings:
# Lecture: *Lecture
# Online: *Lecture - Online Pre-recorded, *Lecture - Online Live, Q&A Session, *Workshop - Online Live
# Workshop: *Workshop
# Computer Workshop: Computer Workshop
# Special: Oral Presentation, Self Study, Examples Class

activity_groups = {
    "*Lecture": ["*Lecture"],
    "*Lecture - Online Pre-recorded": ["*Lecture - Online Pre-recorded", "*Lecture - Online Live", "Q&A Session", "*Workshop - Online Live"],
    "*Lecture - Online Live": ["*Lecture - Online Pre-recorded", "*Lecture - Online Live", "Q&A Session", "*Workshop - Online Live"],
    "Q&A Session": ["*Lecture - Online Pre-recorded", "*Lecture - Online Live", "Q&A Session", "*Workshop - Online Live"],
    "*Workshop - Online Live": ["*Lecture - Online Pre-recorded", "*Lecture - Online Live", "Q&A Session", "*Workshop - Online Live"],
    "*Workshop": ["*Workshop"],
    "Computer Workshop": ["Computer Workshop"],
    "Oral Presentation": ["Oral Presentation"], #TODO: manually add to rooms where it can be held (due to few examples we may miss a lot)
    "Self Study": ["Self Study"], #TODO: manually add to rooms where it can be held (due to few examples we may miss a lot)
    "Examples Class": ["Examples Class"] #TODO: manually add to rooms where it can be held (due to few examples we may miss a lot)
} # TODO: manually check that all rooms have all the activities they can hold, manually add the missing ones

for index, row in df.iterrows():
    room_name = row['Allocated Location Name']
    # room_id = room_ids[room_name]
    activity_type = row['Activity Type Name']
    rooms[room_name].add(activity_type)

# add the missing activities to the rooms (very inefficient, but it's a small dataset)
for room in rooms:
    temp = rooms[room].copy()
    for activity in temp:
        for activity2 in activity_groups[activity]:
            rooms[room].add(activity2)

print("#"*20)
print("ROOMS")
print(rooms) #NOTE
print("#"*20)

# generate the XML file

# create the root element, weeks: 9 to 37, i.e. 29 weeks (9 is included, so is 37), TODO: slotsperday, 5 minute slots, currently gives 24 hrs, should try 9am-5pm or 6pm
root = ET.Element("problem", name="som_timetabling", nrDays="7", nrWeeks="29", slotsPerday="288")

optimization_element = ET.SubElement(root, "optimization", time="2", room="1", distribution="1", student="2")

# create the rooms element
rooms_element = ET.SubElement(root, "rooms")
# for each room, create a room element, with id and capacity
for room in room_ids:
    room_element = ET.SubElement(rooms_element, "room", id=str(room_ids[room]), capacity=str(room_capacities[room_ids[room]]))
    # for each room, create travel times to other rooms
    for room2 in room_ids:
        if room_ids[room] != room_ids[room2]:
            travel_element = ET.SubElement(room_element, "travel", room=str(room_ids[room2]), value=str(travel_times[(room_ids[room], room_ids[room2])][0]))

# create the courses element
courses_element = ET.SubElement(root, "courses")
# for each course, create a course element, with id
for course in courses:
    course_element = ET.SubElement(courses_element, "course", id=course)
    config_element = ET.SubElement(course_element, "config", id=course+"_1")
    lectures = [x[1] for x in subparts[course] if "Lecture" in x[0]]
    for subpart in subparts[course]:
        subpart_element = ET.SubElement(config_element, "subpart", id=subpart[0])
        class_element = ET.SubElement(subpart_element, "class", id=subpart[0]) #TODO: limit, add more copies of the same activity if needed
        # room elements
        for room in rooms:
            if any([x in activity_groups[subpart[1]] for x in rooms[room]]):
                room_element = ET.SubElement(class_element, "room", id=str(room_ids[room]), penalty="0") #TODO: penalty
        #TODO: times for each activity
    # for each course, create a subpart element, with id
    # for subpart, activity, weeks, duration in courses[course]:
    #     subpart_element = ET.SubElement(config_element, "subpart", id=subpart)
        # class_element = ET.SubElement(subpart_element, "activity", id=activity, limit=")
        # weeks_element = ET.SubElement(activity_element, "weeks")
        # for week in weeks:
        #     week_element = ET.SubElement(weeks_element, "week", nr=str(week))

# write XML to file #TODO: re-enable
# with open("som_timetabling.xml", "wb") as file:
#     file.write(ET.tostring(root))

print("#"*20)
print("SUBPARTS")
print(subparts) #NOTE
print("#"*20)

