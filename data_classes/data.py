# <?xml version="1.0" encoding="UTF-8"?>
# <!DOCTYPE problem PUBLIC "-//Course Timetabling Competition//DTD Problem Format/EN" "http://www.unitime.org/interface/competition-format.dtd">
# <!--
# Competition Problem Format
# It includes a unique name of the instance, number of days of the week, number
# of weeks of the semester, and the number of time slots during a days.
# In this example, each time slot takes 5 minutes and they go from
# midnight to midnight. This is typical for all the competition instances,
# however, the problem format allows for variation.
# -->
# <problem name="unique-instance-name" nrDays="7" nrWeeks="13" slotsPerDay="288">
#     <!--
# Optimizatio Weights: These are the weights on the total penalty of assigned
# times, assigned rooms, violated soft distribution constraints,
# and the number of student conflicts.
# -->
#     <optimization time="2" room="1" distribution="1" student="2" />
#     <!--
# List of Rooms: Each room has a unique id, capacity, availability and
# travel times.
# -->
#     <rooms>
#         <room id="1" capacity="50" />
#         <room id="2" capacity="100">
#             <!--
# Travel time to another room is in the number of time slots
# it takes to travel from this room to the other room. All distances are
# symmetrical, and only non-zero distances are present.
# -->
#             <travel room="1" value="2" />
#         </room>
#         <room id="3" capacity="80">
#             <travel room="2" value="3" />
#             <!-- Availability: list of times when the room is not available -->
#             <!-- Not available on Mondays and Tuesdays, 8:30 - 10:30, all weeks -->
#             <unavailable days="1100000" start="102" length="24" weeks="1111111111111" />
#             <!-- Not available on Fridays, 12:00 - 24:00, odd weeks only -->
#             <unavailable days="0001000" start="144" length="144" weeks="1010101010101" />
#         </room>
#         <!-- ... -->
#     </rooms>
#     <!--
# List of Classes that are to be timetabled, including their course structure.
# Each course has one or more configurations, each configuration has one or
# more scheduling subparts, and each subpart has one or more classes.
# All ids are sequentially generated and unique (for each type) within the XML
# file. A class may have a parent id if there is a parent-child relation
# defined.
# -->
#     <courses>
#         <course id="1">
#             <config id="1">
#                 <subpart id="1">
#                     <!--
# Each class has a limit and a list of availabile rooms and times,
# each with a penatly. Only rooms that are big enough and meet all
# the requirements (room type, required equipment, etc.) are listed.
# Each class needs to be assigned to one room and one time from these.
# -->
#                     <class id="1" limit="20">
#                         <room id="1" penalty="0" />
#                         <room id="2" penalty="10" />
#                         <!--
# Each time has days of the week (as bit string, starting on Monday),
# time of the day (start slot and length), and weeks of the semester
# (also a bit string: week 1, week 2, ... ).
# -->
#                         <!-- MWF 7:30 - 8:20 all weeks -->
#                         <time days="1010100" start="90" length="10" weeks="1111111111111"
#                             penalty="0" />
#                         <!-- TTh 8:00 - 9:15 all weeks -->
#                         <time days="0101000" start="96" length="15" weeks="1111111111111"
#                             penalty="2" />
#                     </class>
#                     <!--
# The second class of the same course, configuration, and subpart.
# Alternative to class 1.
# -->
#                     <class id="2" limit="20">
#                         <room id="4" penalty="0" />
#                         <!-- Mon 7:10 - 8:40 even weeks -->
#                         <time days="1000000" start="86" length="18" weeks="0101010101010"
#                             penalty="0" />
#                         <!-- Tue 7:10 - 8:40 even weeks -->
#                         <time days="0100000" start="86" length="18" weeks="0101010101010"
#                             penalty="0" />
#                     </class>
#                 </subpart>
#                 <subpart id="2">
#                     <!--
# Child of class 1: a student taking class 3 must also take class 1.
# Classes may have no rooms, these are only to be assingned with a time.
# -->
#                     <class id="3" parent="1" room="false">
#                         <!-- Fri 8:00 - 9:50 first week -->
#                         <time days="0000100" start="96" length="22" weeks="1000000000000"
#                             penalty="2" />
#                         <!-- Wed 9:00 - 10:50 second week -->
#                         <time days="0010000" start="108" length="22" weeks="0100000000000"
#                             penalty="0" />
#                     </class>
#                     <!-- ... -->
#                 </subpart>
#             </config>
#         </course>
#         <!-- ... -->
#     </courses>
#     <!--
# List of Distribution Constraints: a distribution constraint can be hard
# (required=true) or soft (has a penalty). For most soft constraints,
# a penalty is incurred for each pair of classes that violates the constraint.
# -->
#     <distributions>
#         <!-- Classes 1 and 2 cannot overlap in time -->
#         <distribution type="NotOverlap" required="true">
#             <class id="1" />
#             <class id="2" />
#         </distribution>
#         <!-- Class 1 should be before class 3, class 3 before class 5 -->
#         <distribution type="Precedence" penalty="2">
#             <class id="1" />
#             <class id="3" />
#             <class id="5" />
#         </distribution>
#         <!--
# Instructors are modeled using the SameAttendees constraint: Classes cannot
# overlap in time or be one after the other in rooms that are too far away
# (there are fewer time slots in between than the travel time).
# -->
#         <distribution type="SameAttendees" required="true">
#             <class id="1" />
#             <class id="12" />
#         </distribution>
#         <!-- Classes cannot span more than two days of the week -->
#         <distribution type="MaxDays(2)" required="true">
#             <class id="5" />
#             <class id="8" />
#             <class id="15" />
#         </distribution>
#         <!-- ... -->
#     </distributions>
#     <!--
# Student Course Demands: Each student needs a class of each subpart of one
# configuration of a course. Parent-child relation between classes must be
# used when defined.
# -->
#     <students>
#         <!-- Each student has a list of courses he/she needs. -->
#         <student id="1">
#             <course id="1" />
#             <course id="5" />
#         </student>
#         <student id="2">
#             <course id="1" />
#             <course id="3" />
#             <course id="4" />
#         </student>
#         <!-- ... -->
#     </students>
#     <!--
# Solution: A solution contains a list of classes with their assignments.
# There are also a few solution attributes that can be used to identify the
# solution. These are:
# - problem name (only needed when the XML does not contain the problem,
# i.e., solution is the root element)
# - solver runtime in seconds,
# - number of CPU cores that the solver employs (optional, defaults to 1),
# - name of the solver technique/algorithm,
# - name of the competitor or his/her team,
# - and the name and the country of the institution of the competitor
# -->
#     <solution
#         name="unique-instance-name"
#         runtime="12.3" cores="4" technique="Local Search"
#         author="Pavel Novak" institution="Masaryk University" country="Czech Republic">
#         <!--
# Each class has an assigned time and (when there are rooms) an assigned
# room. Both must be from the domain of the class. There is also a list of
# students enrolled in the class.
# -->
#         <class id="1" days="1010100" start="90" weeks="1111111111111" room="1">
#             <student id="1" />
#             <student id="3" />
#         </class>
#         <class id="2" days="0100000" start="86" weeks="0101010101011" room="4">
#             <student id="2" />
#             <student id="4" />
#         </class>
#         <class id="3" days="0010000" start="108" weeks="0100000000000">
#             <student id="1" />
#         </class>
#         <!-- ... -->
#     </solution>
# </problem>

# the data classes are used to store the data from the xml file

# create a representation of the data in the xml file

class Data:
    def __init__(self, name, nr_days, nr_weeks, slots_per_day, optimization, rooms, courses, distributions, students, solution):
        self.name = name
        self.nr_days = nr_days
        self.nr_weeks = nr_weeks
        self.slots_per_day = slots_per_day
        self.optimization = optimization
        self.rooms = rooms
        self.courses = courses
        self.distributions = distributions
        self.students = students
        self.solution = solution

# create a representation of the optimization in the xml file
        
class Optimization:
    def __init__(self, time, room, distribution, student):
        self.time = time
        self.room = room
        self.distribution = distribution
        self.student = student

# create a representation of the rooms in the xml file
        
class Room:
    def __init__(self, id, capacity, travel, unavailable):
        self.id = id
        self.capacity = capacity
        self.travel = travel
        self.unavailable = unavailable

# create a representation of the travel in the xml file
        
class Travel:
    def __init__(self, room, value):
        self.room = room
        self.value = value

# create a representation of the unavailable in the xml file
        
class Unavailable:
    def __init__(self, days, start, length, weeks):
        self.days = days
        self.start = start
        self.length = length
        self.weeks = weeks

# create a representation of the courses in the xml file
        
class Course:
    def __init__(self, id, config):
        self.id = id
        self.config = config

# create a representation of the config in the xml file
        
class Config:
    def __init__(self, id, subpart):
        self.id = id
        self.subpart = subpart

# create a representation of the subpart in the xml file
        
class Subpart:
    def __init__(self, id, class_):
        self.id = id
        self.class_ = class_

# create a representation of the class in the xml file
        
class Class:
    def __init__(self, id, limit, room, time, parent):
        self.id = id
        self.limit = limit
        self.room = room # constraint object (rather, a list of them)
        self.time = time # constraint object (rather, a list of them)
        self.parent = parent # cause it may be false

# create a representation of the time in the xml file
        
class Time:
    def __init__(self, days, start, length, weeks, penalty):
        self.days = days
        self.start = start
        self.length = length
        self.weeks = weeks
        self.penalty = penalty

# create a representation of the distribution in the xml file
        
class Distribution:
    def __init__(self, type, required, class_):
        self.type = type
        self.required = required
        self.class_ = class_

# TODO: different types of dist. constraints

# create a representation of the student in the xml file
        
class Student:
    def __init__(self, id, course):
        self.id = id
        self.course = course

# create a representation of the solution in the xml file
        
class Solution:
    def __init__(self, name, runtime, cores, technique, author, institution, country, class_):
        self.name = name
        self.runtime = runtime
        self.cores = cores
        self.technique = technique
        self.author = author
        self.institution = institution
        self.country = country
        self.class_ = class_

# create a representation of the class solution (allocation) in the xml file
        
class ClassAllocation:
    def __init__(self, id, days, start, weeks, room, student):
        self.id = id
        self.days = days
        self.start = start
        self.weeks = weeks
        self.room = room
        self.student = student

# create a representation of the student in the class solution (allocation) in the xml file
        
class StudentAllocation:
    def __init__(self, id):
        self.id = id

