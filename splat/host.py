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
from player import *
from client import *

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
		"""Inherits from Client. 'Host' is considered a client
		and simply send the messages to itself."""
		Player.__init__(self, name, color, 'localhost')
		self.availableColors = COLORS
		self.removeColor(color)
		self.clients = [self]

		# setup config
		if config == None:
			self.config = {'boardSize':(10,10), 'maxDots':90, 'maxPlayers':1, 'rounds':1}
		else:
			self.config = config
		# add host
		run_str = "%s:P" % self.color
		print "Host Adding:",run_str
		Run(run_str)

		self.config['maxPlayers'] += 1
		# this should be removed
		# when you have a working Board class
		self.uselessCountVariable = 5

	def beginDotTimer(self):
		self.dotTimer = Timer(DOT_INTERVAL, self.placeNewDots)
		self.dotTimer.start()

	def recvMessage(self, message):
		"""Host receives message from client (request to join,
		request to capture dot, etc.). Determines the form of
		the message, and delegates it accordingly."""

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
		dots_added = []
		#while not self.board.at_max_dots() and len(dots_added) < self.config['maxPlayers'] + 1:
		#	# add dot, track it to send to clients
		#	print "Do i get here?"
		#	dots_added.append(self.board.add_dot)
		for i in xrange(self.config['maxPlayers'] + 1):
			self.board.add_dot()


		# form request and send it out
		#for update in dots_added:
		#	#run_str = "%s:N!%s@%s" % (self.color, str(update[1]), str(update[2]))
		#	#run_str = "%s:N!%2@%2" % (self.color, str(update[1]), str(update[2]))
		#	print "self.color:", self.color
		#	print "update[1]:", str(update[1])
		#	print "update[2]:", update[2]
		#	run_str = "blue:N!" + str(update[1]) + "@" + str(update[2])
		#	print "Run String: ", run_str
		#	Run(run_str)

		#self.uselessCountVariable -= 1
		sys.stderr.write("placeNewDots() has been run\n")

		if not self.board.at_max_dots():
			self.dotTimer = Timer(DOT_INTERVAL, self.placeNewDots)
			self.dotTimer.start()

	def updateClientBoards(self):
		"""This should be used when something is captured,
		and when new dots are added"""
		for client in self.clients:
			client.updateBoard()

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
		# add client to server
		Run("%s:p" % player.color)
		# generate clientBoard
		#player.setBoard(self.board)

	def numClients(self):
		return len(self.clients)

	# refactor this, or something, it's hideous
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
