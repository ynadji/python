#!/usr/bin/env python 

import asyncore
import socket
import httplib
import re
from shared import *
import time
import thread
import random
from operator import *
from array import *
import sys


msg = ''

class Cords():

	cords = "0:0"

	def setCords(self, cords):
		self.cords = cords		

	def getCords(self):
		return str(self.cords)

c = Cords()

class PlayersStruct():

	def __init__(self):
		self.bigboy = {}

	def newColor(self,color):
		self.bigboy[color] = []
		print "New color array created"

	def addMsg(self,color,msg):
		print "New msg added for",color
		self.bigboy[color].append(msg) # insert new msg at the end of the array
		print self.bigboy

	def addMsgAll(self,cords):
		print "Adding cords for everyone"
		for key in self.bigboy.keys():
			self.addMsg(key,cords)
		print self.bigboy

	def countMsg(self,color):
		print self.bigboy
		return len(self.bigboy[color])

	def getMsg(self,color):
		return self.bigboy[color].pop(0)

	
ps = PlayersStruct()

buffer = ''
id = ''
host_color = ''

class Channel(asyncore.dispatcher):

	global buffer

#	def writable (self):
#		print "Writable?"
#		return (len(cords) > 0)
#
#	def readable(self):
#		print "Readable?"
#		return 1

	def checkMsg(self, msg):
		global id
		#try:
		global ps
		global host_color
		# parse the received msg
		id = msg[0:indexOf(msg,"$")]
		color =  msg[len(id)+1:indexOf(msg,":")]
		# we wont always be receiving cords in our msg, so check if we have them or not
		try:
			x_cord = msg[indexOf(msg,"!")+1:indexOf(msg,"@")]
			y_cord = msg[indexOf(msg,"@")+1:]
			print "X:",x_cord
			print "Y:",y_cord
		except Exception:
			pass
		msg = msg[indexOf(msg,":")+1]
		# debug prints
		#print "ID:",id
		print "Color:",color
		print "Msg:",msg

		# create a new player
		if msg[0] == "p":
			print "New player"
			ps.newColor(color)
			c.setCords("You have been added")

		# create the host
		if msg[0] == "P":
			print "New Host"
			ps.newColor(color)
			c.setCords("Got Host? We do.")
			host_color = color

		# Player is requesting any updates in their queuei
		if msg[0] == "U":
			print "Update Found"
			#c.setCords("Updated Cords")
			#print "Msg count:",ps.countMsg(color)
			# We have updates for this player
			if ps.countMsg(color) > 0:
				this_msg = ps.getMsg(color)
				print "Returning this msg:",this_msg
				c.setCords(this_msg)
			# We have no updates for this player
			else:
				c.setCords("Nothing New")
				print "No Messages awaiting"

		# Host player has told us that a new dot exists so we'll add it to the queue for all players
		if msg[0] == "N":
			print "New Dot Cords Received"
			c.setCords("[("+x_cord+","+y_cord+"),'"+color+"','New']")
			cords = c.getCords()
			ps.addMsgAll(cords)
			#print "Awaiting msgs:",ps.countMsg(color)

		if msg[0] == "Q":
			print "Game Over"
			c.setCords("Game Over")
			cords = c.getCords()
			ps.addMsgAll(cords)

		if msg[0] == "C":
			print "Capture attempt"
			c.setCords("[("+x_cord+","+y_cord+"),'"+color+"','Capture']")
			cords = c.getCords()
			ps.addMsg(host_color,cords)

			# Maybe I should write a function that will add all the people trying to capture x y into a queue and when an update board is called we look at the first person in that list and they get the dot.
			# Can be done by using a dict ith x,y keys and whoever is the first value wins it.  Although thats pretty much outside the scope of networking...
			# but where and what hsould I be returning?
		
				#except Exception:
			#pass	

	def handle_read(self):
		global msg
		msg = self.recv (8192)
		self.checkMsg(msg)

	def handle_write(self):
		try:
			global id
			cords = c.getCords()
			cords = cords + "^" # append terminating character
			cords = id + "$" + cords # prepend the ID
			print "ID:",id
			print "Sending msg:",cords
			self.send(cords)
			self.close()
		except Exception:
			pass

		self.close()
		print "---------------------------"

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
		print "Write_lower"
		sent = self.send (self.buffer)
		self.buffer = self.buffer[sent:]

	def handle_read(self):
		print "Read_lower"
		return (len(self.buffer) > 0)
		data = self.recv (8192)


server = Server(8038)
asyncore.loop()
