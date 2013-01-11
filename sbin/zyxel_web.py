#!/usr/bin/python

import requests
from pyquery import PyQuery
import sys

class Zyxel():
	def __init__(self, hostname, username, password):
		self.url = "http://" + hostname + "/"

		# Use session object to login, so we can request diagnostics.cgi
		self.s = requests.session()
		payload = {
			"UserName": username,
			"password": password,
			"hiddenPassword": password,
			"submitValue": 1
		}
		# post once to log in
		r = self.s.post(self.url + "login.cgi", data=payload)

	def nat(self):
		r = self.s.post(self.url + "nat_status.cgi")

		# get the textarea with the info
		p = PyQuery(r.text)
		nat = {}
		for tr in p("table.table_frame > tr"):
			row = [td for td in PyQuery(tr).find('td.table_font')]
			if len(row) > 0:
				print '\t'.join([x.text for x in row])

	def diagnostics(self):
		payload = {
			"DiagDSLStatus": "DSL Line Status",
			"ResetADSLRetryTime": "0"
		}
		r = self.s.post(self.url + "diagnostic.cgi", data=payload)

		# get the textarea with the info
		p = PyQuery(r.text)
		print p("div.infodisplay > textarea").text()

if __name__ == "__main__":
	if len(sys.argv) < 5:
		print "Usage: %s <hostname> <username> <password> <cmd>" % (sys.argv[0],)
		print "  <cmd> is one of: 'nat', 'diagnostics'"
		raise SystemExit

	hostname, username, password, cmd = sys.argv[1:5]
	z = Zyxel(hostname, username, password)
	if cmd == "nat":
		z.nat()
	elif cmd == "diagnostics":
		z.diagnostics()
