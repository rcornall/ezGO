'''
sgfParser.py - helper class
parses sgf files, need to get board posistions  + next move
from sgf games
'''
import sys, os, fnmatch
import sgf # parsing sgf files
import string

from moveState import MoveState
from defines import Defines as defs

# Directory of this file
DIRECTORY = os.path.dirname(os.path.realpath(__file__))

class SGFParser:
    # initialize..
    # walk through directories gathering all SGF files in one big list
    def __init__(self, numberOfGames=99999999):
        self.movesProcessed = 0
        print ("Created Parser, searching for sgf files...")
        self.sgfFilesList = []
        searchPath = os.path.join(DIRECTORY, '..', 'trainingData')
        for root, dirnames, filenames in os.walk(searchPath):
            for filename in fnmatch.filter(filenames, '*.sgf'):
                self.sgfFilesList.append(os.path.join(root, filename))
                if len(self.sgfFilesList) >= numberOfGames:
                    print ("Found %d games." % len(self.sgfFilesList))
                    return
        print ("Found %d games." % len(self.sgfFilesList))
        return


    # Return a list of all the move info per each move from SGFs
    # and the corresponding next move 
    # this data will contain all the necessary info for storing the features later
    # ret: lists of MoveStates for All games (we will split up the data after)
    def get_move_data(self):
        print ("\nBeginning Processing of games:")
        moveData = []

        for game in self.sgfFilesList:
            file = open(game)
            moves = self.parse_game(file.read())
            moveData.extend(moves)

        print("Done processing games.\n")
        return moveData

    # go through a game and get all the required move info
    # ret: list of moveStates for 1 game
    def parse_game(self, sgfGame):
        # list of Move info, contains MoveState objects, plus next moves
        moves = []
        collection = sgf.parse(sgfGame)

        # always 1 game per file..
        for game in collection.children:
            moveState = MoveState()
            for node in game:
                # process each move into a Move object
                ret = self.process_node(moveState, node)
                # print(moveState.board)
                if ret is 0:
                    moves.append(moveState)

        return moves

    #  process 1 SGF move into a managable object
    # ret: 0 - success, 1 skip this move
    def process_node(self, moveState, node):
        sgfMove = node.properties
        # first get the next move and store in MoveState object
        if node.next is not None:
            sgfNextMove = node.next.properties
            if 'B' in sgfNextMove:
                coord = self.parse_coordinate(sgfNextMove.get('B')[0])
                if not coord or len(coord) is 0:
                    return 1
                nextStone = (defs.COLOR.BLACK, coord)
            else:
                coord = self.parse_coordinate(sgfNextMove.get('W')[0])
                if not coord or len(coord) is 0:
                    return 1
                nextStone = (defs.COLOR.WHITE, coord)
            moveState.set_next_move(nextStone)
        else:
            return 1
        # AB and AW are stones positions before the game starts (only on certain games)
        #   so you place all of these initial stones to the board then go from there
        # B and W are regular black and white move coordinates
        # 'stone' includes the color of the stone
        initialStones = []
        stone = ()
        if 'AB' in sgfMove:
            for move in sgfMove.get('AB'):
                coord = self.parse_coordinate(move)
                initialStones.append((defs.COLOR.BLACK,coord))
        elif 'AW' in sgfMove:
            for move in sgfMove.get('AW'):
                coord = self.parse_coordinate(move)
                initialStones.append((defs.COLOR.WHITE,coord))
        elif 'B' in sgfMove:
            coord = self.parse_coordinate(sgfMove.get('B')[0])
            if coord is None or len(coord) is 0:
                # then the move was a 'pass' or skip turn
                return 0
            stone = (defs.COLOR.BLACK, coord)
        elif 'W' in sgfMove:
            coord = self.parse_coordinate(sgfMove.get('W')[0])
            if coord is None or len(coord) is 0:
                # then the move was a 'pass' or skip turn
                return 0
            stone = (defs.COLOR.WHITE, coord)
        else:
            return 1

        if initialStones:
            moveState.place_initial_stones(initialStones)
        else:
            moveState.play_stone(stone)
        self.movesProcessed += 1

        if self.movesProcessed % 100000 == 0:
            print ("\tprocessing... %d moves done" % self.movesProcessed)
        # if self.movesProcessed % 550000 == 0:
        #     print ("\n\texample board state for move %d..." % self.movesProcessed)
        #     print (moveState.board)

        return 0   

    # return integer coordinates from letter coordinates
    def parse_coordinate(self, coord):
        if coord != '' and coord is not None:
            if sys.version_info.major > 3   :
                x = string.lowercase.index(coord[0])
                y = string.lowercase.index(coord[1])
            else:
                x = string.ascii_lowercase.index(coord[0])
                y = string.ascii_lowercase.index(coord[1])
            
            # print(x,y)
            return (x, y)




def test_sgf_parser():
    Parser = SGFParser()
    moveData = Parser.get_move_data()

    FeatureMaker = FeatureMaker()


if __name__ == '__main__':
    test_sgf_parser()
