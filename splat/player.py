#############
# player.py #
#############
# 
# This encapsulates player information and handles communication
# between the host and client. host inherits from player.

# board
# networking
# name
# color
# score
from client import *
from board import *

class Player:

	def __init__(self, name, color, ipAddr):
		self.board = None
		self.ipAddr = ipAddr
		self.name = name
		self.color = color.lower()
		self.score = 0

	def genBoard(self, config):
		"""Makes board lawl"""
		dotsleft = (config['boardSize'][0] * config['boardSize'][1]) - config['maxDots']
		self.board = Board(config['maxPlayers'],
				config['boardSize'][0],
				config['boardSize'][1],
				config['rounds'],
				dotsleft)
		print self.board

	def setBoard(self, board):
		self.board = board

	def addClient(self):
		Run("%s:p" % self.color)

	def recvFromHost(self):
		"""This method receives information from the host
		and delegates to the proper method based on what was received"""
		
	def updateBoard(self):
		"""Updates player's board instance with new information
		received from the Host player"""
		msg = Run("%s:U" % self.color)
		if msg == "Nothing New":
			return
		elif msg == "You have been added":
			return
		elif msg == "Game Over":
			return
		elif msg == "Got Host? We do.":
			return
		"""
		elif msg.startswith("{'maxDots'"):
			self.config = eval(msg)
			self.genBoard(self.config)
		"""

		print "Parsing message:",msg
		infoz = eval(msg)

		# new dot is placed
		if type(infoz).__name__ == 'dict':
			self.config = infoz
			self.genBoard(self.config)
		elif infoz[2] == "New" and infoz[1] == None:
			print "Placing NEW dot"
			x, y = infoz[0]
			self.board.place_dot(x, y, infoz[1])
		elif infoz[2] == "New" and infoz[1] != None:
			print "Dot Capture"
			self.board.claim_dot(infoz[1], infoz[0])
		elif infoz[2] == "Capture":
			print "Capture request to host"
			run_str = str(infoz[1]) + ":N!" + str(infoz[0][0]) + "@" + str(infoz[0][1])
			print "run_str:", run_str
			Run(run_str)

		"""
		if msg.find("None") != -1:
			print "Placing NEW dot"
			coord = eval(msg)
			x, y = coord[0]
			self.board.place_dot(x, y, coord[1])
		else:
			print "Capturing dot"
			coord = eval(msg)
			x, y = coord[0]
			loc = [x,y]
			self.board.claim_dot(coord[1], loc)
		"""


	def dotClicked(self, coords):
		"""Sends request to capture dot at (x,y) to Host"""
		# network.send("DOTCAPTURE", coords)
		run_str = "%s:C!%d@%d" % (self.color, coords[0], coords[1])
		print "Dot Clicked run_str:",run_str
		Run(run_str)

	def updateScore(self, score):
		"""Increments score for current round"""
		if score >= 0:
			self.score += score
