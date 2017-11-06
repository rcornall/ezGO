# sgfParser.py
# parses sgf files, need to get posistions + next move
# from an sgf game

import os, fnmatch
import sgf # parsing sgf files
import string

from moveState import MoveState
from defines import Defines as defs

# Directory of this file
DIRECTORY = os.path.dirname(os.path.realpath(__file__))

class SGFParser:
    # initialize..
    # walk through directories gathering all SGF files in one big list
    def __init__(self):
        self.sgfFilesList = []
        searchPath = os.path.join(DIRECTORY, '..', 'trainingData')
        for root, dirnames, filenames in os.walk(searchPath):
            for filename in fnmatch.filter(filenames, '*.sgf'):
                self.sgfFilesList.append(os.path.join(root, filename))
        # print (self.sgfFilesList)


    # Return a list of all the move info per each move from SGFs
    # and the corresponding next move 
    # this data will contain all the necessary info for storing the features later
    # ret: lists of MoveStates for All games (we will split up the data after)
    def get_move_data(self):
        moveData = []

        for game in self.sgfFilesList:
            file = open(game)
            moves = self.parse_game(file.read())
            moveData.extend(moves)

        return moveData

    # go through a game and get all the required move info
    # ret: list of moveStates for 1 game
    def parse_game(self, sgfGame):
        # list of Move info, contains MoveState objects
        moves = []
        collection = sgf.parse(sgfGame)

        moveState = MoveState()
        # always 1 game per file..
        for game in collection.children:
            for node in game:
                # process each move into a Move object
                move = self.process_node(moveState, node)
                moves.append(move)

        return moves

    #  process 1 SGF move into a managable object 
    # ret: @MoveState
    def process_node(self, moveState, node):
        sgfMove = node.properties
        # AB and AW are stones positions before the game starts (only on certain games)
        #   so you place all of these initial stones to the board then go from there
        # B and W are regular black and white move coordinates
        initialCoords = []
        if 'AB' in sgfMove:
            for stone in sgfMove.get('AB'):
                coord = self.parse_coordinate(stone)
                initialCoords.append(defs.COLOR.BLACK,coord)
        elif 'AW' in sgfMove:
            for stone in sgfMove.get('AW'):
                coord = self.parse_coordinate(stone)
                initialCoords.append(defs.COLOR.WHITE,coord)
        elif 'B' in sgfMove:
            coord = self.parse_coordinate(sgfMove.get('B')[0])
            coord = (defs.COLOR.BLACK, coord)
            print(coord)
        elif 'W' in sgfMove:
            coord = self.parse_coordinate(sgfMove.get('W')[0])
            coord = (defs.COLOR.WHITE, coord)
            print(coord)
        else:
            return None
        
        if initialCoords:
            print("SOME INITAIL COORDINATES ---------------------------------")
            print(initialCoords)
            # place initial stones...
            moveState.place_initial_stones(initialCoords)
            return moveState

        else:
            # play stone on board ...
            moveState.play_stone(coord)
            return moveState


    # return integer coordinates from letter coordinates
    def parse_coordinate(self, coord):
        if coord != "" and coord is not None:
            x = string.lowercase.index(coord[0])
            y = string.lowercase.index(coord[1])
            # print(x,y)
            return (x, y)




def test_sgf_parser():
    Parser = SGFParser()
    moveData = Parser.get_move_data()

if __name__ == '__main__':
    test_sgf_parser()
