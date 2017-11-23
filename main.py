'''
main.py - runnable

runs a loop to receive move input, sends the state of the game to the trained network
the network give a respond move
'''
import os

from defines import Defines as defs
from defines import COLOUR as COLOUR
from network.network import Network
from dataProcessing.moveState import MoveState
from dataProcessing.featureMaker import build_one_move_features


DIRECTORY = os.path.dirname(os.path.realpath(__file__))
CHECKPOINT_DIR = os.path.join(DIRECTORY, 'checkpoints')

if __name__ == '__main__':
    network = Network()
    
    checkpointFile = input("Specify Checkpoint file step (eg 500):\n> ")
    checkpointDir = os.path.join(CHECKPOINT_DIR, "checkpoint_%s" % checkpointFile)
    network.load_checkpoint(checkpointDir)

    moveState = MoveState()
    moveState.play_stone((COLOUR.BLACK, (3,3)))


    while True:
        # default player is black, and network is white
        # get a move
        
        #move = tuple(int(x.strip()) for x in input("Input player move ( eg: 3,3 ):\n> ").split(','))
        #stone = (defs.COLOR.BLACK, move) 
        #moveState.play_stone(stone)

        features = build_one_move_features(moveState)
        responseMove = network.generate_move(features)

        responseMove = network.generate_move(features)

        responseStone = (COLOUR.BLACK, responseMove)

        moveState.play_stone(responseStone)

        print("Board state:")
        print(moveState.board)
        input("show next move...")

        features = build_one_move_features(moveState)
 
        responseMove = network.generate_move(features)

        responseStone = (COLOUR.WHITE, responseMove)

        moveState.play_stone(responseStone)

        print("Board state:")
        print(moveState.board)
        input("show next move...")
        #print(response)


