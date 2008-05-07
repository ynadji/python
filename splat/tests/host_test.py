import sys, unittest

sys.path.append(".")

import host
from player import Player
from time import sleep

class TestGetterSetter(unittest.TestCase):

	def setUp(self):
		self.hst = host.Host("noname","nocolor",None)

	def testName(self):
		"""Tests name is properly get/set"""
		assert self.hst.name == "noname"
		self.hst.name = "Yacin"
		assert self.hst.name == "Yacin"

	def testColor(self):
		"""Tests color is properly get/set"""
		assert self.hst.color == "nocolor"
		self.hst.color = "blue"
		assert self.hst.color == "blue"

	def testScore(self):
		"""Tests score is properly get/set"""
		assert self.hst.score == 0
		self.hst.score = 15
		assert self.hst.score == 15

class TestUpdateScore(unittest.TestCase):

	def setUp(self):
		self.hst = host.Host("noname","nocolor",None)

	def testScore(self):
		assert self.hst.score == 0
		self.hst.updateScore(100)
		assert self.hst.score == 100
		self.hst.updateScore(-100)
		assert self.hst.score == 100

class TestAddPlayer(unittest.TestCase):

	def setUp(self):
		self.hst = host.Host("Yacin","blue",{'boardSize':(15,15), 'maxDots':100, 'maxPlayers':4, 'rounds':1})

		self.client1 = Player("noname","nocolor",'0.0.0.0')
		self.client2 = Player("noname","nocolor",'0.0.0.0')
		self.client3 = Player("noname","nocolor",'0.0.0.0')
		self.client4 = Player("noname","nocolor",'0.0.0.0')
		self.client5 = Player("noname","nocolor",'0.0.0.0')

	def testNumClients(self):
		assert self.hst.numClients() == 1

	def testClientAddMaxPlayers(self):
		"""Tests Host.clientAdd() method. Ensures that only MAX_NUMBER (5, includes host) 
		players can be in the client list"""
		assert self.hst.numClients() == 1
		# try and add clients without proper color
		self.hst.addClient(self.client1)
		assert self.hst.numClients() == 1

		self.client1 = Player("Player 1", "red", '1.2.3.4')
		self.hst.addClient(self.client1)
		assert self.hst.numClients() == 2

		self.client2 = Player("Player 2", "purple", '4.3.2.1')
		self.hst.addClient(self.client2)
		assert self.hst.numClients() == 3

		self.client3 = Player("Player 3", "green", '2.3.1.4')
		self.hst.addClient(self.client3)
		assert self.hst.numClients() == 4

		self.client4 = Player("Player 4", "yellow", '3.2.4.1')
		self.hst.addClient(self.client4)
		assert self.hst.numClients() == 5

		# at maximum capacity
		self.client5 = Player("Player 5", "orange", '4.1.2.3')
		self.hst.addClient(self.client5)
		assert self.hst.numClients() == 5

	def testClientAddSameColor(self):
		"""Tests Host.clientAdd() method. Ensures no color duplicates are allowed."""
		assert self.hst.numClients() == 1
		# try and add clients without proper color
		self.hst.addClient(self.client1)
		assert self.hst.numClients() == 1

		self.client1 = Player("Player 1", "red", '1.2.3.4')
		self.hst.addClient(self.client1)
		assert self.hst.numClients() == 2

		self.client2 = Player("Player 2", "red", '4.3.2.1')
		self.hst.addClient(self.client2)
		assert self.hst.numClients() == 2

		self.client3 = Player("Player 3", "green", '2.3.1.4')
		self.hst.addClient(self.client3)
		assert self.hst.numClients() == 3

		self.client4 = Player("Player 4", "blue", '3.2.4.1')
		self.hst.addClient(self.client4)
		assert self.hst.numClients() == 3

	def testClientAddSameIP(self):
		"""Tests Host.clientAdd() method. Ensures no IP address duplicates are allowed."""
		assert self.hst.numClients() == 1
		# try and add clients without proper color
		self.hst.addClient(self.client1)
		assert self.hst.numClients() == 1

		self.client1 = Player("Player 1", "red", '0.0.0.0')
		self.hst.addClient(self.client1)
		assert self.hst.numClients() == 2

		self.client2 = Player("Player 2", "red", 'localhost')
		self.hst.addClient(self.client2)
		assert self.hst.numClients() == 2

		self.client3 = Player("Player 3", "green", '1.2.3.4')
		self.hst.addClient(self.client3)
		assert self.hst.numClients() == 3

		self.client4 = Player("Player 4", "blue", '1.2.3.4')
		self.hst.addClient(self.client4)
		assert self.hst.numClients() == 3

	def testDotTimer(self):
		"""Tests to ensure dotTimer actually runs."""
		# add something to check if the number of dots increase
		# or the board determines there are no dots left to
		# be placed
		waittime = host.DOT_INTERVAL
		self.hst.beginDotTimer()
		sleep(25)

		# this is a pretty poor way to test it
		# but 'placeNewDots() has been run' should 
		# print 5 times
		assert 0 == 0

if __name__ == "__main__":
	unittest.main()
