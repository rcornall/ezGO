''' 
createTrainingData.py - runnable

Get all the sgf games, parse them move by move into big list,
from this we build 'features' for each move
store this data with 80% for training, and 10% for validation 10% for testing
'''
import os, sys, fnmatch
import time
import numpy as np

DIRECTORY = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIRECTORY, '..'))

from sgfParser import SGFParser
from defines import Defines as defs
import featureMaker


OUT_DIRECTORY = os.path.join(DIRECTORY, '..', 'trainingData', 'processedData')

SAVE_SIZE = 2**14 # save size to save training/testing data in chunks

TrainingTestData = {} # for testing purposes..



# store the data as compressed numpy arrays
def save_data_to_disk(features, nextMoves, dataType, i):
    print("Saving data to disk...")
    save_dict = {}
    save_dict['features'] = features
    save_dict['next_moves'] = nextMoves

    # Split up into test & train sets: (10% testing, 90% training)
    filename = os.path.join(OUT_DIRECTORY, "%s_data.%d" % (dataType, i))
    np.savez_compressed(filename, **save_dict)
    print("saving %s set %d..." % (dataType, i))
    print("done.\n")
    
    # for testing purposes:
    if i == 0 and dataType is "train":
        TrainingTestData = save_dict
    return

# load 1 train file to see if it matches the data before saving
def test_loading():
    print("Try to read data, to check if it was saved properly,")
    filename = os.path.join(OUT_DIRECTORY, "train_data.0.npz")
    npz = np.load(filename)
    print("loaded file: %s/%s" % (OUT_DIRECTORY,filename))
    data = {'features':npz['features'].copy(), 'next_moves':npz['next_moves'].copy()}
    npz.close()


    print("are they the same...")
    np.testing.assert_equal(TrainingTestData, data)
    print("YES\n")


if __name__ == '__main__':
    start_time = time.time()

    Parser = SGFParser(defs.HOW_MANY_GAMES_TO_USE)

    # process 2000 games at a time
    NUMBER_OF_GAMES = 2000
    moveData = Parser.get_some_train_data(NUMBER_OF_GAMES)
    i = 0
    while moveData is not None:
        features, nextMoves = featureMaker.build_features(moveData)
        save_data_to_disk(features, nextMoves, "train", i)
        moveData = Parser.get_some_train_data(NUMBER_OF_GAMES)
        i+=1

    # do the same for test data:
    moveData = Parser.get_some_test_data(NUMBER_OF_GAMES)
    i = 0
    while moveData is not None:
        features, nextMoves = featureMaker.build_features(moveData)
        save_data_to_disk(features, nextMoves, "test", i)
        moveData = Parser.get_some_test_data(NUMBER_OF_GAMES)
        i+=1

    test_loading()
                

    print("Finished in %f secs." % (time.time() - start_time))

