import numpy as np
import os, sys

from defines import Defines as defs
from defines import COLOUR as Colour


<<<<<<< HEAD
colour_names = { Colour.EMPTY: "Empty", Colour.BLACK: "Black", Colour.WHITE: "White"}
inverted_colour = { Colour.EMPTY: Colour.EMPTY, Colour.BLACK: Colour.WHITE, Colour.WHITE: Colour.BLACK}
=======
>>>>>>> fda656845ecf6a8ffb1f6d5c54bb20afa2798732

# Checking if there are any stones adjacent to most recently placed stone
adj_vector_list = [(1,0), (-1,0), (0,1), (0,-1)]

class Group:
	def __init__(self, colour):
		self.Moves = set([])
		self.liberties = set([])
		self.colour = colour

class Board:
	def __init__(self, BOARD_SIZE):
		defs.BOARD_SIZE = defs.BOARD_SIZE
		self.clear()

	def clear(self):
		# Clearing the board and defining Moves to be a tuple of integers
		self.Moves = np.empty((defs.BOARD_SIZE, defs.BOARD_SIZE), dtype = np.int32)
		# Filling the board with "empty" moves
		self.Moves.fill(Colour.EMPTY)
		# Mapping (x,y) tuples to the class Group
		self.possible_moves = []
		self.groups = {}
		# A set of groups
		self.all_groups = set([])
		# A move where there is endless capture and recapture of stones
		self.ko_move = None
		self.FirstMove = Colour.BLACK

	def __getitem__ (self, position):
		return self.Moves[position]

	def check_bounds(self, x_pos, y_pos):
		return x_pos >= 0 and x_pos < defs.BOARD_SIZE and y_pos >= 0 and y_pos < defs.BOARD_SIZE

	# For each pair, there is an list of adjacent pairs
	# Does not yield if out of boundary
	def check_adj(self, pair):
		x_pos, y_pos = pair
		# Using each pair in adj_vector_list and seperating each component of each pair
		for dx,dy in adj_vector_list:
			adj_x, adj_y = x_pos + dx, y_pos + dy
			if self.check_bounds(adj_x, adj_y):
				yield adj_x, adj_y

	# Don't really understand this...
	def combining_groups(self, group1, group2):
		if len(group1.Moves) <len(group2.Moves):
			return self.combining_groups(group2, group1)
		# If not equal, quit
		assert group1.colour == group2.colour
		# Adding group2 stones to group1 and removing group2
		group1.Moves.update(group2.Moves)
		group1.liberties.update(group2.liberties)
		for discarded_moves in group2.Moves:
			self.groups[discarded_moves] = group1
		self.all_groups.remove(group2)
		print("TEST4")
		return group1

	# Remove the group from the set all_groups
	def removing_groups(self, group, changing_colour):
		self.all_groups.remove(group)
		# Delete each pair in groups
		for pair in group.Moves:
			del self.groups[pair]
			# Make the following space "empty"
			#self.Moves[pair] = Colour.EMPTY
			# Checking the adjacent pairs around the current pair
			colour = changing_colour
			for adj_pair in self.check_adj(pair):
				if self.Moves[adj_pair] == changing_colour:
					self.groups[adj_pair].liberties.add(pair)
					print("TEST5")
				else:
					self.Moves[adj_pair] == inverted_colour[colour]

	# Check if okay..
<<<<<<< HEAD
	def check_move(self, x_pos, y_pos, colour, make_move):
		assert colour == Colour.WHITE or colour == Colour.BLACK
=======
	def check_move(self, x_pos, y_pos, color, make_move):
		assert color == colour.WHITE or color == colour.BLACK
>>>>>>> fda656845ecf6a8ffb1f6d5c54bb20afa2798732
		if not (0 <= x_pos < defs.BOARD_SIZE and 0 <= y_pos < defs.BOARD_SIZE): return False
		# Check if a move is being played on top of another stone
		pair = x_pos, y_pos
		if self.Moves[pair] != Colour.EMPTY: return False
		# Checking if there is a KO move
		if self.ko_move and pair == self.ko_move: return  False

<<<<<<< HEAD
		# Creates a group for each stone colour
		group = Group(colour)
=======
		group = Group(color)
>>>>>>> fda656845ecf6a8ffb1f6d5c54bb20afa2798732
		group.Moves.add(pair)

		your_groups = set([])
		to_be_captured_groups = set([])
		self_capture = True

		for adj_pair in self.check_adj(pair):
			# Each move has a set of adjacent spots above, below, left and right of it
			# Tested, added a print statement which prints test for each liberty
			if self.Moves[adj_pair] ==  Colour.EMPTY:
				group.liberties.add(adj_pair)
				self_capture = False
				print("Test1")
				print("Test2: ", len(group.liberties))
			else:
				# Adding groups to form a set of your groups and enemy groups
				# A group for each set of adjacent moves around a stone
				print("test8")
				adj_group = self.groups[adj_pair]
				if self.Moves[adj_pair] == color:
					your_groups.add(adj_group)
					if len(adj_group.liberties) >= 2: self_capture = False
					print("Test: ", len(adj_group.liberties))
				else:
					to_be_captured_groups.add(adj_group)
					if len(adj_group.liberties) == 1: self_capture = False
					print("TEST: ", len(adj_group.liberties))
		# A self-capture move means a vertex has no liberties, adjacent groups of same colour have exactly 1 liberty and all groups of opposite have at least two liberties.
		# Return statements here exit the function
		if self_capture: return False

		# If make_move == False -> Exit function
		if not make_move: return True

		# Make move if legal
		self.Moves[pair] = color
		self.groups[pair] = group
		self.all_groups.add(group)

		# Combining with same colour stones
		print("TEST7")
		for your_group in your_groups:
			print("TEST6")
			your_group.liberties.remove(pair)
			group = self.combining_groups(your_group, group)

		# Capturing opposing stones
		num_stone_captured = 0
		for to_be_captured_group in to_be_captured_groups:
			if len(to_be_captured_group.liberties) == 1:
				num_stone_captured += len(to_be_captured_group.Moves)
				captured_stone = next(iter(to_be_captured_group.Moves))
				self.removing_groups(to_be_captured_group, changing_colour=color)
			else:
				to_be_captured_group.liberties.remove(pair)

		if num_stone_captured == 1 and len(group.Moves) == 1 and len(group.liberties) == 1:
			self.ko_move = captured_stone
		else:
			self.ko_move = None

		self.possible_moves.append(pair)
		self.FirstMove = inverted_colour[color]
		return True

	def player_move(self, x_pos, y_pos, colour):
		if not self.check_move(x_pos, y_pos, colour, make_move=True):
			print("Illegal move.\n")

	def player_move_legal(self, x_pos, y_pos, colour):
		return self.check_move(x_pos, y_pos, colour, make_move=False)

	# When someone passes, you need to clear the ko state
	def skip_turn(self):
		self.ko_move = None
		self.possible_moves.append(None)
		self.FirstMove = inverted_colour[self.FirstMove]

	def display(self):
		colour_str = { Colour.EMPTY: 'E', Colour.BLACK: 'B', Colour.WHITE: 'W'}
		for x_pos in range(defs.BOARD_SIZE): 
			print("[ ", )
			for y_pos in range(defs.BOARD_SIZE):
				if (x_pos,y_pos) == self.ko_move:
					print("x"),
				else:
					print(colour_str[self.Moves[x_pos,y_pos]],)
			print(" ]")
		print ("\n")
		'''
		print
		for y_pos in range(defs.BOARD_SIZE):
			for x in range(defs.BOARD_SIZE):
				if (x_pos,y_pos) == self.ko_move:
					print('x')
				else:
					print ("%s", colour_str[self.Moves[x_pos, y_pos]])
			print
		for x in range (defs.BOARD_SIZE): print("=")
		print
		'''
# The moves being passed here are the total moves that has been played		
def display_seq(board, moves, first_stone_colour):
	board.clear()
	colour = first_stone_colour
	for x_pos,y_pos in moves:
		legal_move = board.player_move(x_pos, y_pos, colour)
		board.display()
		colour = inverted_colour[colour]

def test_Board():
    board = Board(defs.BOARD_SIZE)
    
    print ("simplest capture:")
    display_seq(board, [(1, 0), (0, 0), (0, 1)], Colour.WHITE)
    '''
    print ("move at (0, 0) is legal?", board.player_move_legal(0, 0, Colour.WHITE))
    board.display()
    
    board.flip_colors()
	
    print ("bigger capture:")
    display_seq(board, [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2), (0, 3), (1, 3), (0, 4), (1, 4)], Colour.BLACK)
    
    print ("ko:")
    display_seq(board, [(0, 1), (3, 1), (1, 0), (2, 0), (1, 2), (2, 2), (2, 1), (1, 1)], Colour.BLACK)
    print ("move at (2, 1) is legal?", board.player_move_legal(2, 1, Colour.BLACK))
    board.display()
    board.flip_colors()
    print ("fipped board:")
    board.display()

    print ("self capture:")
    display_seq(board, [(0, 1), (1, 1), (1, 0)], Colour.BLACK)
    print ("move at (0, 0) is legal?", board.player_move_legal(0, 0, Colour.BLACK))

    print ("biffer self capture:")
    display_seq(board, [(1, 0), (0, 0), (1, 1), (0, 1), (1, 2), (0, 2), (1, 3), (0, 3), (1, 4)], Colour.BLACK)
    print ("move at (0, 4) is legal?", board.player_move_legal(0, 0, Colour.WHITE))

'''

if __name__ == "__main__":
    test_Board()
	


