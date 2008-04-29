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

class Player:

	def __init__(self, name, color, ipAddr):
		self.board = "board"
		self.network = "network"
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

	def dotClicked(self, coords):
		"""Sends request to capture dot at (x,y) to Host"""
		# network.send("DOTCAPTURE", coords)

	def updateScore(self, score):
		"""Increments score for current round"""
		if score >= 0:
			self.score += score

	def updateBoard(self, updates):
		"""updates should be a list of a (color,x,y) tuples"""
		for boardCapture in updates:
			#board.capture(boardCapture)
			print "Captured: ", boardCapture
