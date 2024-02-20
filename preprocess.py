import pandas as pd

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

print(room_capacities)

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

print(travel_times)

# (course) : (subpart, activity, weeks)
# TODO: find semester by "Delivery Semester" column for each course
# if empty, check if the course has any other activity with a delivery semester
# also check that all activities of a course have the same delivery semester
# also make sure to take into account the "Number of Teaching Weeks" column
# this can help us find two-semester courses
# for two-semester courses, we can add two courses to the dictionary,
# suffixing the course code with "A" and "B" for the first and second semester, respectively
courses = df['Course Code'].unique()

courses = {course: [] for course in courses}

for index, row in df.iterrows():
    course = row['Course Code']
    subpart = row['Activity Type Name']
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
    dayss = ...
    starts = ...
    penalties = ...
    courses[course].append((subpart, activity, weeks, duration))

print(courses)

# match rooms with possible activity types #TODO: this will probably require some manual work
rooms = {k: set() for k in room_ids.keys()}
activity_types_df = df['Activity Type Name'].unique()
activity_types = set()
for at in activity_types_df:
    activity_types.add(at)

print(activity_types)

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

print(rooms)


