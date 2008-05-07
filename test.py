#!/usr/bin/python

import unittest

import network

ONLINE = "1"
OFFLINE = "0"

class General(unittest.TestCase):

	def testGetIPOnline(self):
		"""Get IP Online"""
		assert network.getIP(ONLINE) != "-1"


	def testGetIPOffline(self):
		"""Get IP Offline"""
		assert network.getIP(OFFLINE) == "-1"


class Host(unittest.TestCase):

	def setUp(self):
		h = network.Host()
		h.startServer()
		print "Hello World"
		print "Hello World"
		print "Hello World"
		print "Hello World"

	def tearDown(self):
		h.killServer()

	def testOMG(self):
		h.killServer()


if __name__ == "__main__":
	unittest.main() # Run all tests
