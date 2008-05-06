#!/usr/bin/env python 

# File: asyncore-example-2.py

import asyncore
import socket, time

# reference time
TIME1970 = 2208988800L

class Channel(asyncore.dispatcher):

    def handle_write(self):
        t = int(time.time()) + TIME1970
        t = chr(t>>24&255) + chr(t>>16&255) + chr(t>>8&255) + chr(t&255)
        self.send(t)
        self.close()

class Server(asyncore.dispatcher):

    def __init__(self, port=37):
        asyncore.dispatcher.__init__(self)
        self.port = port
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(("", port))
        self.listen(5)
        print "listening on port", self.port

    def handle_accept(self):
        channel, addr = self.accept()
        Channel(channel)

server = Server(8037)
asyncore.loop()

