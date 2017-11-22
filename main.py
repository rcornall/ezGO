'''
main.py - runnable

runs a loop to receive move input, sends the state of the game to the trained network
the network give a respond move
'''
import os

from defines import Defines as defs
from network.network import Network
from dataProcessing.moveState import MoveState
from dataProcessing.featureMaker import build_one_move_features


DIRECTORY = os.path.dirname(os.path.realpath(__file__))
CHECKPOINT_DIR = os.path.join(DIRECTORY, 'checkpoints')

if __name__ == '__main__':
    network = Network()
    
    checkpointFile = input("Specify Checkpoint file name (eg checkpoint_500):\n> ")
    checkpointDir = os.path.join(CHECKPOINT_DIR, checkpointFile)
    network.load_checkpoint(checkpointDir)

    moveState = MoveState()


    while True:
        # default player is black, and network is white
        # get a move
        move = tuple(int(x.strip()) for x in input("Input player move ( eg: 3,3 ):\n> ").split(','))

        stone = (defs.COLOR.BLACK, move) 

        moveState.play_stone(stone)

        print("Board state:")
        print(moveState.board)

        features = build_one_move_features(moveState)
 
        responseMove = network.generate_move(features)

        responseStone = (defs.COLOR.WHITE, responseMove)

        moveState.play_stone(responseStone)

        print("Board state:")
        print(moveState.board)
        print("ezGO generated a move: ")
        #print(response)


