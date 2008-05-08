#!/usr/bin/env python 

import asyncore
import socket
import httplib
import re
from shared import *
import time
import thread
import random


msg = ''

class Cords():

	cords = "', 4"

	def setCords(self, cords):
		self.cords = cords		

	def getCords(self):
		return str(self.cords)

c = Cords()

class Channel(asyncore.dispatcher):

	def checkMsg(self, msg):
		try:
			if msg[0] == "U":
				print "Update Found"
				print "Sending Cords"
				c.setCords("Updated Cords")
			if msg[0] == "N":
				print "New Found"
				c.setCords("New Cords")
		except Exception:
			pass	

	def handle_read(self):
		global msg
		msg = self.recv (8192)
		self.checkMsg(msg)

	def handle_write(self):
		try:
			cords = c.getCords()
			cords = cords + "^" # append terminating character
			self.send(cords)
		except Exception:
			pass


class Server(asyncore.dispatcher):

	def __init__(self, port=37):


		self.buffer = "Lawl world"

		asyncore.dispatcher.__init__(self)
		self.port = port
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)

		IP = getIP('0') # Determine the hosts IP address
		ADDR = (IP, port)

		self.bind(ADDR)
		self.listen(5)
		print "listening on ", IP,":",self.port

	def handle_accept(self):
		channel, addr = self.accept()
		Channel(channel)

	def handle_write(self):
		sent = self.send (self.buffer)
		self.buffer = self.buffer[sent:]

	def writable (self):
		return (len(self.buffer) > 0)

	def handle_read(self):
		data = self.recv (8192)

	def readable(self):
		return 1


server = Server(8038)
asyncore.loop()
