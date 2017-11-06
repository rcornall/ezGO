# moveState.py
# 
# object that holds data for a particular turn or move in a game (state of a game)
# data:
#   stone positions (white, black, and empty)
#   Liberties (players and opponents)
#   number of moves so far in the game
#   previous moves in order
#   Kos?
#   whos turn it is

import numpy as np

import defines 
from defines import Defines as defs


class MoveState:
    def __init__(self, board=None):
        if board is not None:
            self.board = board
        else:
            self.board = np.zeros([defs.BOARD_SIZE, defs.BOARD_SIZE], dtype=np.uint8)

    def place_initial_stones(self, coord):
        # ...
        return None

    def play_stone(self, coord):
        # ...
        return None