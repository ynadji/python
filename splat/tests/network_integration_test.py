import sys, unittest

sys.path.append(".")

import player

class TestGetterSetter(unittest.TestCase):

	def setUp(self):
		self.pl = player.Player("noname","nocolor",'0.0.0.0')

	def testName(self):
		"""Tests name is properly get/set"""
		assert self.pl.name == "noname"
		self.pl.name = "Yacin"
		assert self.pl.name == "Yacin"

	def testColor(self):
		"""Tests color is properly get/set"""
		assert self.pl.color == "nocolor"
		self.pl.color = "Blue"
		assert self.pl.color == "Blue"

	def testScore(self):
		"""Tests score is properly get/set"""
		assert self.pl.score == 0
		self.pl.score = 15
		assert self.pl.score == 15

class TestUpdateScore(unittest.TestCase):

	def setUp(self):
		self.pl = player.Player("noname","nocolor",'0.0.0.0')

	def testScore(self):
		assert self.pl.score == 0
		self.pl.updateScore(100)
		assert self.pl.score == 100
		self.pl.updateScore(-100)
		assert self.pl.score == 100

if __name__ == "__main__":
	unittest.main()
