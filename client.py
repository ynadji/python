#!/usr/bin/python

#----------------------#
# Created by Jason Soo #
#      Spring 2008     #
#        CS 487        #
#----------------------#


#----------------------#
#       ERRORS	       #
# -1 : No Internet Con #
#----------------------#

# USE TCP/IP or UDP...


import asyncore, time
import socket
from operator import *

class Client(asyncore.dispatcher):

	def __init__(self, host, msg, port=8038):
		self.buffer = msg
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connect((host, port))

	def writable (self):
		return (len(self.buffer) > 0)

	def handle_write(self):
		sent = self.send (self.buffer)
		self.buffer = self.buffer[sent:]

	def handle_connect(self):
		pass # connection succeeded

	def handle_expt(self):
		self.close() # connection failed, shutdown

	def handle_close(self):
		self.close()

	def handle_read(self):
		# get from server
		s = self.recv(8192)
		print "Received2: ",s[0:indexOf(s,"^")] # We are only interested in the msg, not the repeating msg
		self.handle_write()
		self.handle_close() # we don't expect more data

		
# try it out
request = Client("localhost","U")
asyncore.loop(count = 30)
