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
import numpy as np

import defines 
from defines import Defines as defs


class MoveState:
    def __init__(self, board=None):
        # next move coordinates played after this point in the game
        self.nextMove = ()
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
        self.board[coordinates] = color
        return None

    def set_next_move(self, coordinates):
        self.nextMove = coordinates