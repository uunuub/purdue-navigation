from bs4 import BeautifulSoup
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
    query_url = SCHEDULE_URL + "?" + "days=" + today + "&subject=CS"

    # PoolManager instance to make requests
    http = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())

    # Request page containing schedule
    req = http.request("GET", query_url)
    
    return req.data

    


