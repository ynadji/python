#!/usr/bin/python

import unittest
import server,client

ONLINE = "1"
OFFLINE = "0"

class General(unittest.TestCase):

	#def testGetIPOnline(self):
		#"""Get IP Online"""
		#assert network.getIP(ONLINE) != "-1"


	def testGetIPOffline(self):
		"""Get IP Offline"""
		assert network.getIP(OFFLINE) == "-1"


#class Server(unittest.TestCase):

	#def testStart(self):
		#server()


if __name__ == "__main__":
	unittest.main() # Run all tests
