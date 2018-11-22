from bs4 import BeautifulSoup
from urllib.parse import urlencode
import urllib3.contrib.pyopenssl 
import requests, urllib3, certifi

import logging
logging.basicConfig(level=logging.DEBUG)

# Enable certificate
urllib3.contrib.pyopenssl.inject_into_urllib3()

# Purdue course schedule url
schedule_url = "https://selfservice.mypurdue.purdue.edu/prod/bzwsrch.p_search_schedule?"

# Form query parameters and new url
query_param = {"term": 201910, "subject": "CS"}
url = schedule_url + urlencode(query_param)

# Request page
http = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())
req = http.request("GET", url)
print(req.data)