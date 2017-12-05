'''
moveState.py - data class

object that holds data for a particular turn or move in a game (state of a game)
data:
  stone positions (white, black, and empty)
  Liberties (players and opponents)
  number of moves so far in the game
  previous moves in order
  Kos?
  whos turn it is
  next move coordinates
'''
import sys, os
import numpy as np

# Directory of this file
DIRECTORY = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIRECTORY, '..'))

from defines import Defines as defs



class MoveState:
    def __init__(self, board=None):
        # next move coordinates played after this point in the game
        self.nextMove = ()
        # whos turn to play the next stone
        self.turn = 0
        if board is not None:
            self.board = board
        else:
            self.board = np.zeros([defs.BOARD_SIZE, defs.BOARD_SIZE], dtype=np.uint8)

    # pre-game stones
    def place_initial_stones(self, initialStones):
        if initialStones is None:
            return
        for stone in initialStones:
            color = stone[0]
            coordinates = stone[1]
            self.board[coordinates] = color


    def play_stone(self, stone):
        if stone is None:
            return
        color = stone[0]
        coordinates = stone[1]
        if self.board[coordinates] != defs.COLOR.EMPTY:
            return False
        self.board[coordinates] = color
        return None

    def set_next_move(self, stone):
        self.turn = stone[0]
        self.nextMove = stone[1]

    def check_if_valid(self, x,y):
        coord = (x,y)
        if self.board[coord] != defs.COLOR.EMPTY:
            return False
        else:
            return True


