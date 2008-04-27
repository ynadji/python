#############
# host.py #
#############
# 
# This encapsulates host information and handles communication
# between the host and client. Host -is a- player, but also
# contains routines to send out information to clients, including
# itself.

# TODO:
#	- timer stuff MIGHT need to include mutexes
#	so board isn't altered twice

import sys
from threading import Timer
from player import Player

COLORS = ["blue", "red", "green", "orange", "purple", "yellow"]

# interval used to place dots
# in seconds
DOT_INTERVAL = 5.0

class Host(Player):

	def removeColor(self, color):
		self.availableColors = filter(
				lambda x : x != color, 
				self.availableColors)

	def __init__(self, name, color, config):
		"""Lol inheritance"""
		Player.__init__(self, name, color, 'localhost')
		self.availableColors = COLORS
		self.removeColor(color)
		self.clients = [self]
		self.board

		# setup config
		if config == None:
			self.config = {'boardSize':(10,10), 'maxDots':90, 'maxPlayers':1, 'rounds':1}
		else:
			self.config = config
		# add host

		self.config['maxPlayers'] += 1
		# this should be removed
		# when you have a working Board class
		self.uselessCountVariable = 5

	def beginDotTimer(self):
		self.dotTimer = Timer(DOT_INTERVAL, self.placeNewDots)
		self.dotTimer.start()

	def placeNewDots(self):
		"""Every DOT_INTERVAL, new dots are placed. If the board is full,
		stop recreating the timer thread."""
		"""
		code should look something like this:
		dotsAdded = board.placeNewDots()
		if dotsAdded != 0:
			self.dotTimer = Timer(DOT_INTERVAL, self.placeNewDots)
			self.dotTimer.start()
		"""
		self.uselessCountVariable -= 1
		sys.stderr.write("placeNewDots() has been run\n")

		# this is temporary until i have a working Board
		# class. Board should return the number of dots added
		# or something similar, and the Timer threads
		# will no longer be made after all possible
		# dots have been added
		if self.uselessCountVariable > 0:
			self.dotTimer = Timer(DOT_INTERVAL, self.placeNewDots)
			self.dotTimer.start()

	#def updateBoard(self, request):

	def addClient(self, player):
		if len(self.clients) == self.config['maxPlayers']:
			sys.stderr.write("Error: Cannot have more than " + str(self.config['maxPlayers']) + " players in Splat!\n")
			return

		if not self.availableColors.__contains__(player.color):
			sys.stderr.write("Error: Two players cannot both use the color \"" + player.color + "\". Select a different color\n.")
			return

		if not self.nameFree(player.name):
			sys.stderr.write("Error: Two players cannot both use the name \"" + player.name + "\". Select a different name\n.")
			return

		if not self.ipFree(player.ipAddr):
			sys.stderr.write("Error: Two players cannot both use the IP Address \"" + player.ipAddr + "\"\n.")
			return

		self.clients.append(player)
		self.removeColor(player.color)

	def numClients(self):
		return len(self.clients)

	# refactor this, or something
	def nameFree(self, name):
		free = True
		for player in self.clients:
			if player.name == name:
				free = False

		return free

	def ipFree(self, ipAddr):
		free = True
		for player in self.clients:
			if player.ipAddr == ipAddr:
				free = False

		return free
