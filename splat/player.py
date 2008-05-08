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

class Player:

	def __init__(self, name, color, ipAddr):
		self.board = "board"
		self.ipAddr = ipAddr
		self.name = name
		self.color = color.lower()
		self.score = 0

	def recvFromHost(self):
		"""This method receives information from the host
		and delegates to the proper method based on what was received"""
		
	def updateBoard(self):
		"""Updates player's board instance with new information
		received from the Host player"""
		msg = Run("%s:U" % self.color)
		#if 

	def dotClicked(self, coords):
		"""Sends request to capture dot at (x,y) to Host"""
		# network.send("DOTCAPTURE", coords)
		Run("%s:c!%d@%d" % (self.color, coords[0], coords[y])

	def updateScore(self, score):
		"""Increments score for current round"""
		if score >= 0:
			self.score += score
