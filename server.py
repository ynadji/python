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

	def setCords(self):
		self.cords = "",random.randint(1, 10)
		#self.cords = "5"

	def getCords(self):
		return str(self.cords)

c = Cords()

class Channel(asyncore.dispatcher):

	def checkMsg(self, msg):
		if msg[0] == "U":
			print "Update Found"

	def handle_read(self):
		global msg
		msg = self.recv (8192)
		print "Server Reading:", msg
		print msg
		self.checkMsg(msg)

	def handle_write(self):
		#self.handle_read()
		cords = "12"
		print "Server: Hello Channel"
		cords = c.getCords()
		cords = "Cords"
		self.send(cords)
		#self.send(c.getCords())
		time.sleep(.1)
		#c.setCords()
		self.close()


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
		print "Channel: ",channel
		#x = "Hello Client"
		#self.send(x)
		Channel(channel)

	def handle_write(self):
		print "Server Writing"
		#cords = "12-4"
		#self.cords = cords
		sent = self.send (self.buffer)
		self.buffer = self.buffer[sent:]
		#self.close()

	def writable (self):
		return (len(self.buffer) > 0)

	def handle_read(self):
		print "Server Reading"
		data = self.recv (8192)
		print data

	def readable(self):
		print "Server: To read or not to read..."
		return 1


	def handle_connect (self):
		print "Server: Hello Client"
		self.send("Hello Client")


#def Run():
server = Server(8038)
asyncore.loop()
#thread.start_new_thread(asyncore.loop(),count = 40)

#def Run():
	#while (1):
		#thread.start_new_thread(asyncore.poll,())
		#thread.start_new_thread(asyncore.loop,())
		#asyncore.poll(timeout=.01)
		#time.sleep(2)


#thread.start_new_thread(Run(),'')
#print "Hello World"
