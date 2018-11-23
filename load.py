from urllib.parse import urlencode
import urllib3.contrib.pyopenssl 
import requests, urllib3, certifi

from bs4 import BeautifulSoup
import datetime

from app import db
from models import Time, Instructor, Type, Room, Building, CRN, Number, Name, Course

# Uncomment to enable debug requests
# import logging
# logging.basicConfig(level=logging.DEBUG)

# Purdue course schedule url
SCHEDULE_URL = "https://selfservice.mypurdue.purdue.edu/prod/bzwsrch.p_search_schedule"

def getToday():
	# Get current day numbeR
	weekdays = ("M", "T", "W", "R", "F", "S", "U")
	# Current date
	return weekdays[datetime.datetime.today().weekday()]

def getSchedule():
	# Get today one character form
	today = getToday()

	# Enable certificate
	urllib3.contrib.pyopenssl.inject_into_urllib3()

	# Form query url with current day
	params = {"days": today, "subject": "CS"}
	query_url = SCHEDULE_URL + "?" + "days=" + today + "&subject=CS"

	# PoolManager instance to make requests
	http = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())

	# Request page containing schedule
	req = http.request("GET", query_url)
	
	return req.data

def parseSchedule(raw_sched):
	# Get scraped schedule page
	html = BeautifulSoup(raw_sched, "html5lib")

	# Find the text content within th tags and split them by "-" to get course titles
	course_titles = []
	for tag in html.findAll("th", {"class": "ddlabel"}):
		# Current course titles	
		current = [] 
		for content in tag.a.contents[0].split("-"):
			current.append(content.strip(" "))	
		# Split Subject & Number	
		current = current[:2] + current[2].split(" ") + current[3:]
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
		# Add course to collection
		course_details.append(current)	

	# Remove first element since it's not a course table	
	course_details = course_details[1:]

	return course_titles, course_details

def storeSchedule(titles, details):
	for i, j in zip(titles, details):
		print(i + j)
	return	


