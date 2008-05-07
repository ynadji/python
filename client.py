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

class Client(asyncore.dispatcher):

	def __init__(self, host, port=8038):
		self.buffer = "Hello Server"
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connect((host, port))

	def writable (self):
		return (len(self.buffer) > 0)

	def handle_write(self):
		self.buffer = "New Dots? - Client"
		#print "Client: Checking for new dots"
		sent = self.send (self.buffer)
		self.buffer = self.buffer[sent:]

	def handle_connect(self):
		print "Client: Connected"
		pass # connection succeeded

	def handle_expt(self):
		self.close() # connection failed, shutdown

	def handle_read(self):

		# get from server
		s = self.recv(4)
		print "Received: ",s

		#self.handle_close() # we don't expect more data

	def handle_close(self):
		self.close()

	def adjust_time(self, delta):
		# override this method!
		print "k", delta

	def handle_read(self):
		# get from server
		s = self.recv(4)
		print "Received: ",s
		time.sleep(.1)
		self.handle_write()

		



# try it out
#def Run():
request = Client("localhost")
asyncore.loop(count = 2)
