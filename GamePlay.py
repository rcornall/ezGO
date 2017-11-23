import numpy as np
import os, sys

from defines import Defines as defs
from defines import COLOUR as colour

# FIGURE OUT HOW TO LINK THE TWO FILES
#DIRECTORY = os.path.dirname(os.path.realpath(__file__))
#sys.path.insert(0, os.path.join(DIRECTORY))

class colour:
    EMPTY = 0
    BLACK = 1
    WHITE = 2

colour_names = { colour.EMPTY: "Empty", colour.BLACK: "Black", colour.WHITE: "White"}
inverted_colour = { colour.EMPTY: colour.EMPTY, colour.BLACK: colour.WHITE, colour.WHITE: colour.BLACK}

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
		self.Moves.fill(colour.EMPTY)
		# Mapping (x,y) tuples to the class Group
		self.possible_moves = []
		self.groups = {}
		# A set of groups
		self.all_groups = set([])
		# A move where there is endless capture and recapture of stones
		self.ko_move = None
		self.FirstMove = colour.BLACK

	def __getitem__ (self, position):
		return self.Moves[position]

	def check_bounds(self, x_pos, y_pos):
		return x_pos >= 0 and x_pos < defs.BOARD_SIZE and y_pos >= 0 and y_pos < defs.BOARD_SIZE

	# For each pair, there is an list of adjacent pairs
	def check_adj(self, pair):
		x_pos, y_pos = pair
		# Using each pair in adj_vector_list and seperating each component of each pair
		for dx,dy in adj_vector_list:
			adj_x, adj_y = x + dx, y + dy
			if self.check_bounds(adj_x, adj_y):
				yield adj_x, adj_y

	# Don't really understand this...
	def combining_groups(self, group1, group2):
		if len(group.Moves) <len(group2.Moves):
			return self.combining_groups(group2, group1)
		# If not equal, quit
		assert group1.colour == group2.colour
		# Adding group2 stones to group1 and removing group2
		group1.Moves.update(group1.Moves)
		group1.liberties.update(group2.liberties)
		for discarded_moves in group2.Moves:
			self.groups[discarded_moves] = group1
		self.all_groups.remove(group2)
		return group1

	# Remove the group from the set all_groups
	def removing_groups(self, group, changing_colour):
		self.all_groups.remove(group)
		# Delete each pair in groups
		for pair in group.Moves:
			del self.groups[pair]
			# Make the following space "empty"
			self.Moves[pair] = colour.EMPTY
			# Checking the adjacent pairs around the current pair
			for adj_pair in self.check_adj(pair):
				if self.Moves[adj_pair] == changing_colour:
					self.groups[adj_pair].liberties.add(pair)

	# Check if okay..
	def check_move(self, x_pos, y_pos, colour, make_move):
		assert colour == colour.WHITE or colour == colour.BLACK
		if not (0 <= x_pos < defs.BOARD_SIZE and 0 <= y_pos < defs.BOARD_SIZE): return False
		# Check if a move is being played on top of another stone
		pair = x_pos, y_pos
		if self.Moves[pair] != colour.EMPTY: return False
		# Checking if there is a KO move
		if self.ko_move and pair == self.ko_move: return  False

		group = Group(colour)
		group.Moves.add(pair)

		your_groups = set([])
		to_be_captured_groups = set([])
		self_capture = True
		for adj_pair in self.check_adj(pair):
			if self.Moves[adj_pair] ==  colour.EMPTY:
				group.liberties.add(adj_pair)
				self_capture = False
			else:
				# Adding groups to form a set of your groups and enemy groups
				adj_group = self.groups[adj_pair]
				if self.Moves[adj_pair] == colour:
					your_groups.add(adj_group)
					if len(adj_group.liberties) >= 2: self_capture = False
				else:
					to_be_captured_groups.add(adj_group)
					if len(adj_group.liberties) == 1: self_capture = False
		# A self-capture move means a vertex has no liberties, adjacent groups of same colour have exactly 1 liberty and all groups of opposite have at least two liberties.
		if self_capture: return False

		if not make_move: return True

		# Make move if legal
		self.Moves[pair] = colour
		self.groups[pair] = group
		self.all_groups.add(group)

		# Combining with same colour stones
		for your_group in your_groups:
			your_group.liberties.remove(pair)
			group = self.combining_groups(your_group, group)

		# Capturing opposing stones
		num_stone_captured = 0
		for to_be_captured_group in to_be_captured_groups:
			if len(to_be_captured_group.liberties) == 1:
				num_stone_captured += len(to_be_captured_group.Moves)
				captured_stone = next(iter(to_be_captured_group.Moves))
				self.removing_groups(to_be_captured_group, changing_colour=colour)
			else:
				to_be_captured_group.liberties.remove(pair)

		if num_stone_captured == 1 and len(group.Moves) == 1 and len(group.liberties) == 1:
			self.ko_move = captured_stone
		else:
			self.ko_move = None

		self.possible_moves.append(pair)
		self.FirstMove = inverted_colour[colour]
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
		colour_str = { colour.EMPTY: 'E', colour.BLACK: 'B', colour.WHITE: 'W'}
		for x_pos in range(defs.BOARD_SIZE): print(" =")
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

def display_seq(board, moves, first_stone_colour):
	board.clear()
	colour = first_stone_colour
	for x_pos,y_pos in moves:
		legal_move = board.player_move(x_pos, y_pos, colour)
		board.display()
		colour = inverted_colour[colour]

def test_Board():
    board = Board(5)
    
    print ("simplest capture:")
    display_seq(board, [(1, 0), (0, 0), (0, 1)], colour.BLACK)
    '''
    print ("move at (0, 0) is legal?", board.player_move_legal(0, 0, colour.WHITE))
    board.display()
    
    board.flip_colors()

    print ("bigger capture:")
    display_seq(board, [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2), (0, 3), (1, 3), (0, 4), (1, 4)], colour.BLACK)

    print ("ko:")
    display_seq(board, [(0, 1), (3, 1), (1, 0), (2, 0), (1, 2), (2, 2), (2, 1), (1, 1)], colour.BLACK)
    print ("move at (2, 1) is legal?", board.player_move_legal(2, 1, colour.BLACK))
    board.display()
    board.flip_colors()
    print ("fipped board:")
    board.display()

    print ("self capture:")
    display_seq(board, [(0, 1), (1, 1), (1, 0)], colour.BLACK)
    print ("move at (0, 0) is legal?", board.player_move_legal(0, 0, colour.BLACK))

    print ("biffer self capture:")
    display_seq(board, [(1, 0), (0, 0), (1, 1), (0, 1), (1, 2), (0, 2), (1, 3), (0, 3), (1, 4)], colour.BLACK)
    print ("move at (0, 4) is legal?", board.player_move_legal(0, 0, colour.WHITE))

'''

if __name__ == "__main__":
    test_Board()
	


