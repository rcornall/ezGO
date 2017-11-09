''' 
createTrainingData.py - runnable

Get all the sgf games, parse them move by move into big list,
from this we build 'features' for each move
store this data with 80% for training, and 10% for validation 10% for testing
'''
import sys, os, fnmatch
import time
import numpy as np

from sgfParser import SGFParser
from defines import Defines as defs
import featureMaker

DIRECTORY = os.path.dirname(os.path.realpath(__file__))
OUT_DIRECTORY = os.path.join(DIRECTORY, '..', 'trainingData', 'processedData')

# store the data as compressed numpy arrays
def save_data_to_disk(features, nextMoves):
    sys.stdout.write("Saving data to disk...")
    save_dict = {}
    save_dict['features'] = features
    save_dict['next_moves'] = nextMoves

    filename = os.path.join(OUT_DIRECTORY, "train_data.%d" % 1)
    #print "NPZ.RandomizingWriter: writing", filename
    np.savez_compressed(filename, **save_dict)
    print("done.\n")
    return save_dict

def test_loading(saved_dict):
    print("Try to read data, to check if it was saved properly,")
    for root, dirnames, filenames in os.walk(OUT_DIRECTORY):
            for filename in fnmatch.filter(filenames, '*.npz'):
                npz = np.load("%s/%s" % (OUT_DIRECTORY,filename))
                print("loaded file: %s/%s" % (OUT_DIRECTORY,filename))
                data = {'features':npz['features'].copy(), 'next_moves':npz['next_moves'].copy()}
                npz.close()


    print("are they the same...")
    np.testing.assert_equal(saved_dict, data)
    print("YES\n")


if __name__ == '__main__':
    start_time = time.time()

    Parser = SGFParser(defs.HOW_MANY_GAMES_TO_USE)
    moveData = Parser.get_move_data()

    features, nextMoves = featureMaker.build_features(moveData)
    del moveData # try to clear up some space

    data = save_data_to_disk(features, nextMoves)
    del features
    del nextMoves

    # try loading and check the contents are the same as before saving them..
    test_loading(data)
                

    print("Finished in %f secs." % (time.time() - start_time))

