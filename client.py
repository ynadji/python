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


import asyncore
import socket

class Client(asyncore.dispatcher):

    def __init__(self, host, port=8038):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))

    def writable(self):
        return 0 # don't have anything to write

    def handle_connect(self):
        pass # connection succeeded

    def handle_expt(self):
        self.close() # connection failed, shutdown

    def handle_read(self):

        # get from server
        s = self.recv(4)
	print "Received: ",s
        delta = "balls"

        self.handle_close() # we don't expect more data

    def handle_close(self):
        self.close()

    def adjust_time(self, delta):
        # override this method!
        print "k", delta

# try it out

request = Client("localhost")

asyncore.loop()
