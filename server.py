#!/usr/bin/env python 

# File: asyncore-example-2.py

import asyncore
import socket, time
import httplib

# reference time
TIME1970 = 2208988800L

class Channel(asyncore.dispatcher):

	def handle_write(self):
		t = int(time.time()) + TIME1970
		t = chr(t>>24&255) + chr(t>>16&255) + chr(t>>8&255) + chr(t&255)
		self.send(t)
		self.close()

def getIP(online):
	# This is statement is only used for 
	if online == "0":
		return "-1"
	try:
		conn = httplib.HTTPConnection("www.showmyip.com")
		conn.request("GET","/")
		r1 = conn.getresponse()
		data1 = r1.read()
		p = re.compile("[\d\+\.]{7,15}")
		results = p.findall(data1)
		ip = results[0]
		return ip
	except:
		return "-1"
		raise
	


class Server(asyncore.dispatcher):

	def __init__(self, port=37):
		asyncore.dispatcher.__init__(self)
		self.port = port
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)

		IP = getIP("1") # Determine the hosts IP address

		ADDR = (IP, port)

		print "ADDR: ",ADDR

		self.bind(ADDR)
		#self.bind((IP, port))
		self.listen(5)
		print "listening on port", self.port

	def handle_accept(self):
		channel, addr = self.accept()
		Channel(channel)

server = Server(8037)
asyncore.loop()

