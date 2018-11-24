from app import db
from models import Time, Instructor, Type, Room, Building, CRN, Number, Name, Course, Subject

from urllib.parse import urlencode
import urllib3.contrib.pyopenssl 
import requests, urllib3, certifi

from bs4 import BeautifulSoup
import datetime

import pandas as pd
import pprint

# Uncomment to enable debug requests
# import logging
# logging.basicConfig(level=logging.DEBUG)

# Purdue course schedule url
SCHEDULE_URL = "https://selfservice.mypurdue.purdue.edu/prod/bzwsrch.p_search_schedule"

def clear_data(session):
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
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
	query_url = SCHEDULE_URL + "?" + "days=" + today + "&subject=CS"	
	
	# Log queried url
	print(query_url)

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
			if len(td.contents) == 1:
				current += td.contents	
			# Avoid additionall tags within instructor tags	
			else:
				current.append(td.contents[0][:-2])	

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
	headers = ["name", "crn", "subj", "number", "time", "days", "location", "date", "type", "instructor"]
	df = pd.DataFrame(course_info, columns=headers)
	# Currently there is no need for #8 - Start, End Date
	df.drop(columns=["date"], inplace=True)

	# Change time column to list of datetime.time()s
	start, end = df["time"].str.split(" - ").str
	start = start.apply(lambda stime: datetime.datetime.strptime(stime, "%I:%M %p").time())
	end = end.apply(lambda stime: datetime.datetime.strptime(stime, "%I:%M %p").time())
	df["time"] = tuple(pd.concat([start, end], axis=1).values.tolist())

	# Split location column into building and room
	df["building"], df["room"] = df["location"].str.rsplit(" ", 1).str
	df.drop(columns=["location"], inplace=True)

	return df

def load(session, df):
	print(df.to_string())
	# Add to database unique values
	uniques = {}
	for col in df:
		# Get unique values of a column
		uniques[col] = df[col].unique().tolist()

	pp = pprint.PrettyPrinter(indent=4)
	#pp.pprint(uniques)


	# Write unique values to database
	for k, vals in uniques.items():
		for v in vals:		
			if k == "name":
				session.add(Name(name=v))
			elif k == "number":
				session.add(Number(number=v))
			elif k == "crn":
				session.add(CRN(crn=v))
			elif k == "building":
				session.add(Building(building=v))
			elif k == "subject":
				session.add(Subject(Subject=v))
			elif k == "instructor":
				session.add(Instructor(instructor=v))
			elif k == "type":
				session.add(Type(stype=v))
			elif k == "room":
				session.add(Room(room=v))
			elif k == "building":
				session.add(Building(building=v))
			elif k == "time":
				continue
				# session.add(Type(type=v)
	session.commit()

