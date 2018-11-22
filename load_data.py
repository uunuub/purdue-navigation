from bs4 import BeautifulSoup
from contextlib import closing
from urllib.parse import urlencode

import urllib3.contrib.pyopenssl 
import requests, urllib3, certifi

import datetime
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

def parseSchedule():
	# Get scraped schedule page
	raw_sched = getSchedule()
	html = BeautifulSoup(raw_sched, "html5lib")

	# Find the text content within th tags and split them by "-" to get course titles
	course_titles = []
	for tag in html.findAll("th", {"class": "ddlabel"}):
		current_course = [] 
		for content in tag.a.contents[0].split("-"):
			current_course.append(content.strip(" "))
		course_titles.append(current_course)
	for i in course_titles:
		print(i)

	# Find all course details
	course_details = []
	for tag in html.findAll("table", {"class": "datadisplaytable"}):
		# Skip if it's not a course tr tag
		if(len(tag.contents) < 3):
			continue
		current_course = []
		# Get all td tags within course tr tag
		for td in tag.tbody.findNext("tr").findNext("tr").findAll("td"):
			if len(td.contents) == 1:
				current_course += td.contents	
			# Avoid additionall tags within instructor tags	
			else:
				current_course.append(td.contents[0][:-2])
		course_details.append(current_course)	
	
	# for i in course_details:
	# 	print(i)

parseSchedule() 


