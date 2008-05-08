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

	# Create players
	def testClientCreate(self):
		assert Run("green:P") == "You have been added"

	def testClientCreate2(self):
		assert Run("blue:P") == "You have been added"

	def testClientCreate2(self):
		assert Run("red:P") == "You have been added"

	# Add new dot
	def testNewDotCord(self):
		assert Run("red:N!1@1") == "1,1"

	# All plays get correct cords of new dot?
	def testNewDotUpdate(self):
		assert Run("green:U") == "1,1"

	def testNewDotUpdate2(self):
		assert Run("blue:U") == "1,1"

	def testNewDotUpdate3(self):
		assert Run("red:U") == "1,1"

	# Make sure we have nothing new for all players now
	def testNewDotUpdate4(self):
		assert Run("red:U") == "Nothing New"

	def testNewDotUpdate5(self):
		assert Run("green:U") == "Nothing New"

	def testNewDotUpdate6(self):
		assert Run("blue:U") == "Nothing New"

	# Try to capture dot
	def testCaptureDot(self):
		assert Run("green:C!1@1") == ""



if __name__ == "__main__":
	unittest.main() # Run all tests
