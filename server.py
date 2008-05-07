#!/usr/bin/env python 

import asyncore
import socket
import httplib
import re
from shared import *


class Channel(asyncore.dispatcher):

	def handle_write(self):
		cords = "12-4"
		self.send(cords)
		self.close()



class Server(asyncore.dispatcher):

	def __init__(self, port=37):
		asyncore.dispatcher.__init__(self)
		self.port = port
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)

		IP = getIP('1') # Determine the hosts IP address
		ADDR = (IP, port)

		self.bind(ADDR)
		self.listen(5)
		print "listening on port", self.port

	def handle_accept(self):
		channel, addr = self.accept()
		Channel(channel)

#server = Server(8038)
#asyncore.loop()
