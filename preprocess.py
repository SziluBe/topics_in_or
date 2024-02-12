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



