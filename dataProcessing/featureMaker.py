'''
featureMaker.py - helper functions

from a list of MoveStates (or states of the board + next move)
build feature arrays for different important inputs to use for training 

3x features for stone positions (player, opponent, empty)


'''
import numpy as np

from defines import Defines as defs

PLANES=3

def build_features(moveData):
    print("Building features.\n")

    features = np.zeros([len(moveData), defs.BOARD_SIZE, defs.BOARD_SIZE, 3], dtype=np.uint8)
    nextMoves = np.zeros([len(moveData), defs.BOARD_SIZE, defs.BOARD_SIZE], dtype=np.uint8)

    for i, move in enumerate(moveData):
        colorFeatures = makeColorFeatures(move)
        features[i] = colorFeatures
        nextMoves[i, move.nextMove[0], move.nextMove[1]] = 1    

    return features, nextMoves

def makeColorFeatures(moveData):
    # features is an array composed of 3 board sized arrays 
    # (player stones, opponent stones, empty spots)
    features = np.zeros([defs.BOARD_SIZE, defs.BOARD_SIZE, 3], dtype=np.uint8)
    if moveData.turn == defs.COLOR.BLACK:
        features[moveData.board == defs.COLOR.BLACK, 0] = 1
        features[moveData.board == defs.COLOR.WHITE, 1] = 1
    else:
        features[moveData.board == defs.COLOR.WHITE, 0] = 1
        features[moveData.board == defs.COLOR.BLACK, 1] = 1
    features[moveData.board == defs.COLOR.EMPTY, 2] = 1
    
    # print("\n\n0th Feature:")
    # print(features[:,:,0])
    # print("\n\n1th Feature:")
    # print(features[:,:,1])
    # print("\n\n2th Feature:")
    # print(features[:,:,2])

    return features
