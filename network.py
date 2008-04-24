#!/usr/bin/python

#----------------------#
# Created by Jason Soo #
#      Spring 2008     #
#        CS 487        #
#----------------------#


# USE TCP/IP or UDP...


# Create a socket to be used over the network
from socket import * 
import thread

def handler(clientsock, addr):
	while 1:
		data = clientsock.recv(BUFSIZ)
		if not data: break 
		clientsock.send(data)

	clientsock.close()


if __name__=='__main__':
	#HOST = 'localhost'
	HOST = '216.47.133.103'
	PORT = 21567
	BUFSIZ = 1024
	ADDR = (HOST, PORT)
	serversock = socket(AF_INET, SOCK_STREAM)
	serversock.bind(ADDR)
	serversock.listen(2)

	while 1:
		print 'waiting for connection...'
		clientsock, addr = serversock.accept()
		print '...connected from:', addr
		#Thread.__init__(self, handler, (clientsock,addr))
		thread.start_new_thread(handler, (clientsock,addr))

	serversock.close()
