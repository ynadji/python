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
		assert Run("orange:P") == "You have been added"

	def testClientCreate3(self):
		assert Run("red:P") == "You have been added"

	# Add new dot
	def testNewDotCord(self):
		assert Run("red:N!2@2") == "2,2"

	def testNewDotCord2(self):
		assert Run("red:N!3@3") == "3,3"

	def testNewDotCord3(self):
		assert Run("red:N!1@1") == "1,1"

	# All plays get correct cords of new dot?
	def testNewDotUpdate(self):
		assert Run("green:U") == "2,2"

	def testNewDotUpdate2(self):
		assert Run("orange:U") == "2,2"

	def testNewDotUpdate3(self):
		assert Run("red:U") == "2,2"

	def testNewDotUpdate4(self):
		assert Run("red:U") == "3,3"

	def testNewDotUpdate5(self):
		assert Run("green:U") == "3,3"

	def testNewDotUpdate6(self):
		assert Run("orange:U") == "3,3"

	# Try to capture dot
	#def testCaptureDot(self):
		#assert Run("green:C!1@1") == ""

	def testNewDotCord4(self):
		assert Run("red:N!-1@-1") == "-1,-1"

#class GameOver(unittest.TestCase):
	#def testGameOver10(self):
		#assert Run("green:Q") == "Game Over"

if __name__ == "__main__":
	unittest.main() # Run all tests
