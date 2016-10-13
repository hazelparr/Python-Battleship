BOARD_SIZE = 10
EMPTY = 'O'

class Board:
	def __init__(self):
		board = [[EMPTY for x in range(10)] for y in range(10)]
		self.board = board
		
	

	def print_board_heading(self):
		print("   " + " ".join([chr(c) for c in range(ord('A'), ord('A') + BOARD_SIZE)]))

	def print_board(self):
		self.print_board_heading()

		row_num = 1
		for row in self.board:
			print(str(row_num).rjust(2) + " " + (" ".join(row)))
			row_num += 1