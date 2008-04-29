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


# Create a socket to be used over the network
from socket import * 
import thread
import httplib
import re

ONLINE = "1"
OFFLINE = "0"


# This method makes the server multi-threaded.
def handler(clientsock, addr):
	while 1:
		data = clientsock.recv(BUFSIZ)
		if not data: break 
		clientsock.send(data)

	clientsock.close()

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
	

# The host class
class Host:

	def __init__(self):

		print "Welcome"

	def startServer(self):

		# Run a method to get the IP address here.
		# Set the IP found to the host.

		HOST = getIP(ONLINE)
		PORT = 21567
		BUFSIZ = 1024
		ADDR = (HOST, PORT)
		serversock = socket(AF_INET, SOCK_STREAM)
		serversock.bind(ADDR)
		serversock.listen(2)

		# Loop and away incoming connections.  As they are
		# received spawn a thread to service them.
		while 1:
			print 'waiting for connection on ',HOST,'...'
			clientsock, addr = serversock.accept()
			print '...connected from:', addr
			thread.start_new_thread(handler, (clientsock,addr))

		serversock.close()




class Client:

	def __init__(self):

		# Run a method to get the IP address here.
		# Set the IP found to the host.

		HOST = getIP(ONLINE)
		PORT = 21567
		BUFSIZ = 1024
		ADDR = (HOST, PORT)

		tcpCliSock = socket(AF_INET, SOCK_STREAM)
		tcpCliSock.connect(ADDR)

		# Loop through and away user input to send accross the wire.
		# Should be able to remove this and only send data accross
		# the wire as needed (on demand).  Hopefully the client doesnt
		# need to bind a socket in order to receive data on demand.
		while 1:
			data = raw_input('> ')
			if not data: break 
			tcpCliSock.send(data)
			data = tcpCliSock.recv(1024)
			if not data: break 
			print data

		tcpCliSock.close()

class Network:

	def simDeadConn():
		getIP(OFFLINE)
