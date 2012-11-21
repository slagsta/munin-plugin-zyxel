#!/usr/bin/python

import requests
from pyquery import PyQuery
import sys

if len(sys.argv) < 2:
	print "Usage: %s <hostname> <username> <password>" % (sys.argv[0],)
	raise SystemExit

url = "http://" + sys.argv[1] + "/"
username = sys.argv[2]
password = sys.argv[3]

# Use session object to login, so we can request diagnostics.cgi
s = requests.session()
payload = {
	"UserName": username,
	"password": password,
	"hiddenPassword": password,
	"submitValue": 1
}
r = s.post(url + "login.cgi", data=payload)

# request diagnostics
payload = {
	"DiagDSLStatus": "DSL Line Status",
	"ResetADSLRetryTime": "0"
}
r = s.post(url + "diagnostic.cgi", data=payload)

# get the textarea with the info
p = PyQuery(r.text)
print p("div.infodisplay > textarea").text()
