from models import Time, Instructor, Type, Room, Building, CRN, Number, Name, Course, Subject

from urllib.parse import urlencode
import urllib3.contrib.pyopenssl 
import requests, urllib3, certifi

from bs4 import BeautifulSoup
import datetime

import pandas as pd

# Uncomment to enable debug requests
# import logging
# logging.basicConfig(level=logging.DEBUG)

# Purdue course schedule url
SCHEDULE_URL = "https://selfservice.mypurdue.purdue.edu/prod/bzwsrch.p_search_schedule"

def clear_data(session, metadata):
	for table in reversed(metadata.sorted_tables):
		session.execute(table.delete())
	session.commit()

"""Gets current day in one character notation

Returns:
	string -- A character indicating current day
"""
def getToday():
	# Get current day number, ignored weekends
	weekdays = ("M", "T", "W", "R", "F", "F", "F")
	
	# Current date
	return weekdays[datetime.datetime.today().weekday()]

"""Scrapes Purdue's schedules website for current day's courses

Returns:
	string -- raw html file of schedule website
"""
def getSchedule():
	# Get today one character form
	today = getToday()

	# Enable certificate
	urllib3.contrib.pyopenssl.inject_into_urllib3()

	# Form query url with current day
	params = {"days": today, "subject": "CS"}
	query_url = SCHEDULE_URL + "?" + "days=" + today
	
	# Log queried url
	# print(query_url)

	# PoolManager instance to make requests
	http = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())

	# Request page containing schedule
	req = http.request("GET", query_url)
	
	return req.data

"""Parses raw html file containing schedule

Returns:
	list -- list contains course related information:
			name, crn, subject, course number, time, days, 
			building, start and end date, class type, intstructor
"""
def parseSchedule(raw_sched):
	# Let beautifulsoup parse html
	html = BeautifulSoup(raw_sched, "html5lib")

	# Find the text content within th tags and split them by "-" to get course titles
	course_titles = []
	for tag in html.findAll("th", {"class": "ddlabel"}):
		# Current course titles	
		current = [] 
		for content in tag.a.contents[0].split(" - "):
			current.append(content.strip(" "))	
		# Split Subject & Number	
		current = current[:2] + current[2].split(" ") + current[3:]
		# Remove last element, class number
		current.pop(len(current) - 1)
		
		# Add course to collection
		course_titles.append(current)
	
	# Find all course details
	course_details = []
	for tag in html.findAll("table", {"class": "datadisplaytable"}):
		# Skip if it's not a course tr tag
		if(len(tag.contents) < 3):
			continue

		current = []
		# Get all td tags within course tr tag
		for td in tag.tbody.findNext("tr").findNext("tr").findAll("td"):
			# If content has more tags, means it's insturctor tag
			if len(td.contents) > 1:
				current.append(td.contents[0][:-2])
			# Check if tag is TBA tag
			elif td.contents[0].find("TBA") != -1:
				current.append("TBA")
			# Concatenate if it's just other tags
			elif len(td.contents) == 1:
				current += td.contents	

		# Remove first element, a literal string "Class"
		current.pop(0)
		# Add course to collection
		course_details.append(current)	

	# Remove first element since it's not a course table	
	course_details.pop(0)
	# Combine lists by columns
	return list(map(lambda a, b: (a + b), course_titles, course_details))


def storeSchedule(course_info):
	# Parameter must be a list of lists each 10 elements:
	# 0: Name
	# 1: CRN
	# 2: Subject
	# 3: Number
	# 4: Start, End Time
	# 5: Days
	# 6: Building & Room
	# 7: Start, End Date. NOTE: Different from #3
	# 8: Class Type
	# 9: Instructor

	# for i in course_info:
	# 	print(i)

	# We will be utilizing pandas for easier manipulation
	headers = ["name", "crn", "subject", "number", "time", "days", "location", "date", "stype", "instructor"]
	df = pd.DataFrame(course_info, columns=headers)

	# Currently there is no need for #8 - Start, End Date
	df.drop(columns=["date"], inplace=True)

	# Change time column to list of datetime.time()
	start, end = df["time"].str.split(" - ").str
	start = start.apply(lambda stime: datetime.datetime.strptime(stime, "%I:%M %p").time())
	end = end.apply(lambda stime: datetime.datetime.strptime(stime, "%I:%M %p").time())
	df["time"] = tuple(pd.concat([start, end], axis=1).values.tolist())

	# Split location column into building and room
	df["building"], df["room"] = df["location"].str.rsplit(" ", 1).str
	df.drop(columns=["location"], inplace=True)

	# Drop rows with NaN
	df.dropna(inplace=True)

	return df

def load(session, df):
	# Add to database unique values
	uniques = {}
	for col in df:
		# Get unique values of a column
		uniques[col] = df[col].unique().tolist()

	# Dictionary containing class objects
	models = {
		"name": Name,
		"number": Number,
		"crn": CRN,
		"building": Building,
		"subject": Subject,
		"instructor": Instructor,
		"stype": Type,
		"room": Room
	}

	# Write unique values to database
	for k, vals in uniques.items():
		if k == "days":
			continue
		if k == "time":
			for v in vals:		
				session.add(Time(start_time=v[0], end_time=v[1]))
		else:
			for v in vals:		
				session.add(models[k](**{k: v}))
	session.commit()


	print(df.to_string())
	# Iterate over each courses
	for index, row in df.iterrows():
		# Set room to point to building
		building = Building.query.filter_by(building=row["building"]).first()
		room = Room.query.filter_by(room=row["room"]).first()
		building.rooms.append(room)

		session.add(Course(name_id=Name.query.filter_by(name=row["name"]).first().id,
							number_id=Number.query.filter_by(number=row["number"]).first().id,
							subject_id=Subject.query.filter_by(subject=row["subject"]).first().id,
							crn_id=CRN.query.filter_by(crn=row["crn"]).first().id,
							building_id=building.id,
							room_id=room.id,
							type_id=Type.query.filter_by(stype=row["stype"]).first().id,
							instructor_id=Instructor.query.filter_by(instructor=row["instructor"]).first().id,
							time_id=Time.query.filter_by(start_time=row["time"][0], end_time=row["time"][1]).first().id,
							days=row["days"]))	
		session.commit()

	# print(Building.query.filter(Building.building == "Felix Haas Hall").first().rooms)