from player import *
from host import *
from board import *
import time
from random import randint

def genBoard(config):
	"""Makes board lawl"""
	dotsleft = (config['boardSize'][0] * config['boardSize'][1]) - config['maxDots']
	board = Board(config['maxPlayers'],
			config['boardSize'][0],
			config['boardSize'][1],
			config['rounds'],
			dotsleft)

	return board

config = {'boardSize':(10,10), 'maxDots':90, 'maxPlayers':2, 'rounds':1}
initial_board = genBoard(config)

h = Host("yacin","blue",config)
time.sleep(2)
p1 = Player("jason","orange",'23.45.32.13')
p2 = Player("balls","yellow",'24.45.32.13')

h.setBoard(initial_board)
p1.setBoard(initial_board)
p2.setBoard(initial_board)

h.addClient(p1)
p1.addClient()
time.sleep(2)
h.addClient(p2)
p2.addClient()
time.sleep(2)

print h.board
print p1.board
print p2.board

print "===== Loopz ====="
h.beginDotTimer()

while True:
	h.updateClientBoards()

	print h.board
	print p1.board
	print p2.board
	print p2.board.grid

	time.sleep(1)
	h.dotClicked((randint(0,9),randint(0,9)))
	p1.dotClicked((randint(0,9),randint(0,9)))
	p2.dotClicked((randint(0,9),randint(0,9)))
	time.sleep(2)
