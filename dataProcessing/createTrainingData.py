''' 
createTrainingData.py - runnable

Get all the sgf games, parse them move by move into big list,
from this we build 'features' for each move
store this data with 80% for training, and 10% for validation 10% for testing
'''
import time

from sgfParser import SGFParser
from defines import Defines as defs
import featureMaker

# store the data as compressed numpy arrays
def save_data_to_disk(features, nextMoves):
    print("Saving data to disk...")
    # ...
    return

if __name__ == '__main__':
    start_time = time.time()

    Parser = SGFParser(defs.HOW_MANY_GAMES_TO_USE)
    moveData = Parser.get_move_data()

    features, nextMoves = featureMaker.build_features(moveData)

    save_data_to_disk(features, nextMoves)

    print("Finished in %f secs." % (time.time() - start_time))

