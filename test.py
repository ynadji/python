#!/usr/bin/python

import unittest
from client import *
from shared import *

ONLINE = "1"
OFFLINE = "0"

class General(unittest.TestCase):

	#def testGetIPOnline(self):
		#"""Get IP Online"""
		#assert network.getIP(ONLINE) != "-1"
	pass


class Player(unittest.TestCase):

	def testClientCreate(self):
		Client("localhost","green:P")

	def testClientCreate2(self):
		assert Client("localhost","blue:P") == "You have been added"

if __name__ == "__main__":
	unittest.main() # Run all tests
