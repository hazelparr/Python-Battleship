from player import Player
from board import Board
import os

VERTICAL_SHIP = '|'
HORIZONTAL_SHIP = '-'
MISS = '.'
HIT = '*'
SUNK = '#'	


def ascii_art():
	ascii_art = '''
______       _   _   _           _     _       
| ___ \     | | | | | |         | |   (_)      
| |_/ / __ _| |_| |_| | ___  ___| |__  _ _ __  
| ___ \/ _` | __| __| |/ _ \/ __| '_ \| | '_ \ 
| |_/ / (_| | |_| |_| |  __/\__ \ | | | | |_) |
\____/ \__,_|\__|\__|_|\___||___/_| |_|_| .__/ 
                                        | |    
                                        |_|    
'''
	return ascii_art

def prompt_location(player, ship_type, ship_size):
	'''aks the player for location in the board and validates
	if in correct format, calls function again if not and prints
	error message'''
	if ship_type == None:
		location = input("\n{}, select your target: ".format(player.name)).strip()
	else:
		location = input("\n{}, select location of the {} ({} spaces): ".format(player.name, ship_type, ship_size)).strip()
	if is_loc_valid(location):
		return location
	else:
		print("\nError! Must have letters A - J and numbers 1 - 10. For example: G7")
		input("Press enter to continue.")
		clear()
		if ship_type == None:
			player.gameboard.print_board()
			return prompt_location(player, ship_type, ship_size)
		else:
			player.board.print_board()
			return prompt_location(player, ship_type, ship_size)


def is_loc_valid(location):
	'''checks location format and returns True if in correct format'''
	valid_letters = "abcdefghij"
	valid_numbers = "123456789"
	if len(location) == 3:
		if location[0].lower() in valid_letters and location[1:] == "10":
			return True
	elif len(location) == 2:
		if location[0].lower() in valid_letters and location[1] in valid_numbers:
			return True
	else:
		return False
	

def prompt_orientation():
	'''checks if orientation input is correct if not, calls
	function again and prints error message'''
	orientation = input("Is the ship horizontal(h) or vertical(v)? ").strip()
	if orientation.lower() == "v" or orientation.lower() == "h":
		return orientation
	else:
		print("Error! Please enter 'h' for horizontal or 'v' for vertical.")
		return prompt_orientation()


def is_orientation_valid(orientation, location, ship_size):
	'''checks if the ship will fit board based on orientation input'''
	if orientation.lower() == "h":
		if ord(location[0].lower()) + ship_size <= ord("k"):
			return True
		else:
			return False
	else:
		if int(location[1:]) - 1 + ship_size <= 10:
			return True
		else:
			return False

def convert_locs(location):
	'''converts input location to a tuple of board coordinates'''
	row_ind = ord(location[0].lower()) - ord("a")
	col_ind = int(location[1:]) - 1
	return row_ind, col_ind


def get_ship_locs(location, orientation, ship_size):
	'''Returns a tuple of all the coordinates the ship
	occupies in the board'''
	ship_locs = []
	#row_ind, col_ind = convert_locs(location)
	row_ind = ord(location[0].lower()) - ord("a")
	col_ind = int(location[1:]) - 1
	index = 0
	if orientation == "h":
		for i in range(ship_size):
			ship_locs.append((row_ind + index, col_ind))
			index += 1
	else:
		for i in range(ship_size):
			ship_locs.append((row_ind, col_ind + index))
			index += 1
	return ship_locs


def ship_overlap(ship_locs, ships):
	'''check if there is an overlap with another ship in the board'''
	for item in ship_locs:
		for item2 in ships:
			if item in item2.positions:
				return True


def update_board(player, ship_locs, orientation):
	'''updates board with the location input from player'''
	for loc in ship_locs:
		if orientation == "h":
			player.board.board[loc[1]][loc[0]] = HORIZONTAL_SHIP
		else:
			player.board.board[loc[1]][loc[0]] = VERTICAL_SHIP
			

def place_ships(player, ships):
	'''place ships on board once all validations are ok'''
	clear()
	player.board.print_board()
	location = prompt_location(player, ships.ship_type, ships.size)
	orientation = prompt_orientation().lower()

	if not is_orientation_valid(orientation, location, ships.size):
		print("\nError! Ship does not fit the board. Enter another location or orientation.")
		input("Press enter to continue.")
		place_ships(player, ships)
	else:
		ship_locs = get_ship_locs(location, orientation, ships.size)
	
		if ship_overlap(ship_locs, player.ships):
			print("\nError! Ship overlaps with previously placed ship. Choose another location.")
			input("Press enter to continue.")
			place_ships(player, ships)
		else:
			ships.positions.extend(ship_locs)
			update_board(player, ship_locs, orientation)


def clear():
	'''clears screen whenever called'''
	if os.name == "nt":
		os.system("cls")
	else:
		os.system("clear")

def is_ship_hit(player, ships, shot_loc):
	'''checks if shot hits opponent's ship. Returns
	which type of ship was hit'''
	for ship in ships:
		if shot_loc in ship.positions:
			#print("You HIT {}'s {}".format(player.opponent.name, ship.ship_type))
			return ship

def update_game_board(player, coord, char):
	'''updates player's current game board'''
	player.gameboard.board[coord[1]][coord[0]] = char


def is_ship_sunk(ship_hit):
	'''checks the health of the ship'''
	if ship_hit.health == 0:
		return ship_hit.positions


def shoot_turns(players):
	'''Players take turns shooting on opponent's boards.
	Returns winning player'''
	while True:
		for player in players:
			clear()
			player.gameboard.print_board()
			shot_loc = prompt_location(player, None, None)
			shot_loc = convert_locs(shot_loc)
			
			while shot_loc in player.shots_location:
				clear()
				print("You already fired in this location. Try another one.\n")
				player.gameboard.print_board()
				shot_loc = prompt_location(player, None, None)
				shot_loc = convert_locs(shot_loc)
			
			player.shots_location.append(shot_loc)

			if is_ship_hit(player, player.opponent.ships, shot_loc): #shot_loc in ship.positions:
				clear()
				ship_hit = is_ship_hit(player, player.opponent.ships, shot_loc)
				print("\nYou HIT {}'s {}!\n".format(player.opponent.name, ship_hit.ship_type))
				ship_hit.health -= 1
				
				
				if is_ship_sunk(ship_hit):
					player.sunk += 1
					print("Excellent shot! {}'s {} is now SUNKED!\n".format(player.opponent.name, ship_hit.ship_type))
					sunk_coords = is_ship_sunk(ship_hit)
					
					for coords in sunk_coords:
						update_game_board(player, coords, SUNK)
					player.gameboard.print_board()
					
					if player.sunk == 5:
						input("\nAll of {}'s ships are now sunked. Press enter to continue. ".format(player.opponent.name))
						clear()
						return player
					else:
						input("\nPress enter to continue. ")

				else:
				# ship hit but not sunked yet
					update_game_board(player, shot_loc, HIT)
					player.gameboard.print_board()
					input("\nPress enter to continue.")
					clear()
			else:
				clear()
				update_game_board(player, shot_loc, MISS)
				player.gameboard.print_board()
				input("\nYou missed! Better luck next time. Press enter to continue.")

def game():
	clear()
	print(ascii_art())
	print("\nPlayer 1")
	Player1 = Player()
	print("\nPlayer 2")
	Player2 = Player()

	Player1.opponent = Player2
	Player2.opponent = Player1
	players = (Player1, Player2)

	#asks players to place their ships
	input("\nPlayers, get ready to enter the location of your ships. Press enter to continue.")
	clear()
	for player in players:
		#player.board.print_board()
		for ships in player.ships:
			place_ships(player, ships)
			clear()
			player.board.print_board()
		input("\nYou have placed all your ships. Press enter to continue.")
	
	#battle commences
	clear()
	input("Let the battles commence! Press enter to continue.")
	clear()
	
	winner = shoot_turns(players)

	print("\nCongratulations {}! You have demolished {}'s entire fleet.".format(winner.name, winner.opponent.name))
	print("\n{}, you are the WINNER!".format(winner.name))
	input("\nPress enter to see both player boards.")
	clear()
	# display boards
	print("\n{}'s board: \n".format(Player1.name))
	Player1.board.print_board()
	print("\n{}'s board: \n".format(Player2.name))
	Player1.board.print_board()

	input("\nPress enter to quit the game. Thanks for playing.")




if __name__ == "__main__":
	game()