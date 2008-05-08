#################
# high_score.py #
#################
# 
# This class handles storing high score information in a db
# and displaying the information on a server.

import time
import BaseHTTPServer
import sqlite3
import cgi
from socket import gethostbyname, gethostname

HOST_NAME = gethostbyname(gethostname()) # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8080 # Maybe set this to 9000.
SERVER_PASS = 'awesome'

# lame hack to get 'Incorrect password' to show up
global pass_correct
pass_correct = True

class ServerHandler(BaseHTTPServer.BaseHTTPRequestHandler):

	def do_HEAD(self):
		"""Sends headers"""
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()

	def do_POST(self):
		"""Respond to a POST request. If the password inputted is correct,
		display the high score information."""
		
		ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
		length = int(self.headers.getheader('content-length'))

		qs = self.rfile.read(length)
		v = cgi.parse_qs(qs, keep_blank_values=1)
		global pass_correct

		if v['passwd'][0] == SERVER_PASS:
			pass_correct = True
			# get info from DB
			db_string = "<center><table border='4' width=50%><tr><td><b>User Handle</b></td><td><b>Score</b></td></tr>"
			conn = sqlite3.connect('./scores.db')
			c = conn.cursor()
			c.execute('SELECT * FROM high_scores ORDER BY score DESC LIMIT 25')
			numscores = 0
			for score_ent in c:
				numscores += 1
				db_string += "<tr><td>%s</td><td>%s</td></tr>" % (score_ent[0], score_ent[1])

			db_string += '</table></center>'

			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()
			header = "<html> <head> <title>High Scores</title> </head> <body> <center><h1><p>Top %d Scores on %s</p></h1></center> <br />" % (numscores, HOST_NAME)
			footer = "</body></html>"
			self.wfile.write(header)
			self.wfile.write(db_string)
			self.wfile.write(footer)
		else:
			pass_correct = False
			self.do_GET()

	def do_GET(self):
		"""Displays form for password access. Runs do_POST when submit is clicked."""
		global pass_correct
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()

		header = "<html><head><title>High Scores Page</title></head><body><center><h1><p>High Scores Database</p></h1></center><br />"
		if pass_correct:
			form = "<form method='POST'>Password:<input type='password' name='passwd'><input type='submit' value='Submit'></form>"
		else:
			form = "<form method='POST'>Password:<input type='password' name='passwd'><input type='submit' value='Submit'><br /><font color='red'>Incorrect password</font></form>"

		footer = "</body></html>"
		self.wfile.write(header)
		self.wfile.write(form)
		self.wfile.write(footer)

def startserver():
	"""Starts server."""
	server_class = BaseHTTPServer.HTTPServer
	httpd = server_class((HOST_NAME, PORT_NUMBER), ServerHandler)
	print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
		httpd.server_close()
		print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

def addhighscore(handle, score):
	"""Adds highscore. If database doesn't exist, create the
	database/table layout, and add the high score"""
	conn = sqlite3.connect('./scores.db')
	c = conn.cursor()
	try:
		c.execute("INSERT INTO high_scores VALUES('%s',%d)" % (handle, score))
	except sqlite3.OperationalError:
		c.execute("CREATE TABLE high_scores (handle VARCHAR(25), score INTEGER);")
		c.execute("INSERT INTO high_scores VALUES('%s',%d)" % (handle, score))
	conn.commit()
	c.close()
	conn.close()

def clearhighscores():
	"""Deletes highscore table and recreates it."""
	conn = sqlite3.connect('./scores.db')
	c = conn.cursor()
	try:
		c.execute("DROP TABLE high_scores")
	finally:
		c.execute("CREATE TABLE high_scores (handle VARCHAR(25), score INTEGER);")
		conn.commit()
		c.close()
		conn.close()

if __name__ == '__main__':
	startserver()
