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
import random

id = ''
complete_msg = ''
received = ''

class Client(asyncore.dispatcher):


	def __init__(self, host, msg, first = "true", port=8038):
		print "-----------------------------"
		global id
		global complete_msg
		if first == "true":
			id = random.getrandbits(20)
			id = "%d" % id
			self.buffer = id + "$" + msg
		else:
			self.buffer = msg
		complete_msg = self.buffer
		print self.buffer
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
		global received
		self.close()
		print "Returning:",received
		#raise received
		#return received

	def handle_read(self):
		global id
		global complete_msg
		global received
		# get from server
		s = self.recv(8192)
		rid = s[0:indexOf(s,"$")]
		print "Received ID:",rid
		print "Sent ID:",id
		if rid != id:
			print "RECEIVED A DIFFERENT ID THAN WE SENT!!!!"
			#self.buffer = complete_msg
			print "RESENDING:",complete_msg
			request = Client("localhost",complete_msg,first= "false") # set resend to true
			# ???????? die here, don't come back and exec more code
			pass

		print "Received2: ",s[len(rid)+1:indexOf(s,"^")] # We are only interested in the msg, not the repeating msg
		self.handle_write()
		received = s[len(rid)+1:indexOf(s,"^")]
		self.handle_close() # we don't expect more data

def Run(msg):
	request = Client("localhost",msg) # Add a new player
	asyncore.loop(count = 30)
	return received

		
# try it out
#request = Client("localhost","green:P") # Add a new player
#asyncore.loop(count = 30)
#request = Client("localhost","blue:P") # Add a new player
#asyncore.loop(count = 30)
#request = Client("localhost","green:N!1@1") # host is sending us cords for new dots
#asyncore.loop(count = 30)
#request = Client("localhost","green:N!2@2") # host is sending us cords for new dots
#asyncore.loop(count = 30)
#request = Client("localhost","green:N!3@3") # host is sending us cords for new dots
#asyncore.loop(count = 30)
#request = Client("localhost","green:U") # player is requesting cords for new dots or captured dots
#asyncore.loop(count = 30)
#request = Client("localhost","green:U") # player is requesting cords for new dots or captured dots
#asyncore.loop(count = 30)
#request = Client("localhost","green:U") # player is requesting cords for new dots or captured dots
#asyncore.loop(count = 30)
#request = Client("localhost","green:U") # player is requesting cords for new dots or captured dots
#asyncore.loop(count = 30)
#request = Client("localhost","green:C!1@1") # player has tried to capture dot at x y cord
#asyncore.loop(count = 30)
