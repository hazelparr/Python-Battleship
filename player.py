from ships import Ships
from board import Board
		
BOARD_SIZE = 10
EMPTY = 'O'

SHIP_INFO = [
    ("Aircraft Carrier", 5),
    ("Battleship", 4),
    ("Submarine", 3),
    ("Cruiser", 3),
    ("Patrol Boat", 2)
]

class Player:
	def init_ship(self):
		self.ships = []
		for ship in SHIP_INFO:
			self.ships.append(Ships(ship[0], ship[1]))

	def __init__(self):
		name = input("Enter name: ")
		self.name = name
		self.board = Board()
		self.gameboard = Board()
		self.init_ship()
		self.opponent = None
		self.shots_location = []
		self.sunk = 0