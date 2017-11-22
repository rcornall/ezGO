''' 
train.py - runnable

Train the neural net
'''

import os, sys, fnmatch
import time

import numpy as np
import tensorflow as tf

DIRECTORY = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIRECTORY, '..'))

from network.network import Network
from defines import Defines as defs

BATCH_SIZE=64
DATA_DIRECTORY = os.path.join(DIRECTORY, '..', 'trainingData', 'processedData')
CHECKPOINT_DIR = os.path.join(DIRECTORY, '..', 'checkpoints')

def read_data(file):
    numpyFile = np.load(file)
    features = numpyFile['features']
    nextMoves = numpyFile['next_moves']
    numpyFile.close()
    return features, nextMoves

def get_files(dataType="train"):
    inputDataFilesList = []
    for root, dirnames, filenames in os.walk(DATA_DIRECTORY):
        for filename in fnmatch.filter(filenames, '%s*.npz' % dataType):
            inputDataFilesList.append(os.path.join(root, filename))
    return inputDataFilesList

def get_batch(features, nextMoves, batch_size=BATCH_SIZE):
    batch = {}
    batch['features'] = features[:batch_size]
    batch['next_moves'] = nextMoves[:batch_size]
    return batch

if __name__ == '__main__':
    start_time = time.time()


    inputDataFilesList = get_files("train")
    print("Found %d training data files" % len(inputDataFilesList))

    with tf.device('/cpu:0'):
        with tf.Graph().as_default():
            network = Network()
            checkpointFile = input("Specify Checkpoint file name (eg checkpoint_500):\n> ")
            checkpointDir = os.path.join(CHECKPOINT_DIR, checkpointFile)
            network.load_checkpoint(checkpointDir)
            i=0
            for file in inputDataFilesList:
                features, nextMoves = read_data(file)
                print("Total feature size is %d, Total next move size is %d" %(len(features), len(nextMoves)))
                batch = get_batch(features, nextMoves, BATCH_SIZE)
                while len(batch['features']) != 0:
                    # train 1 batch at a time:
                    network.train(batch)


                    if i%5 == 0:
                        network.average_summary()

                    if i%100==0 and i!=0:
                        network.save_checkpoint(CHECKPOINT_DIR, network.get_global_step())
                    
                    # get rid of the data used in previous batch
                    # and get the next batch
                    features = features[BATCH_SIZE:]
                    nextMoves = nextMoves[BATCH_SIZE:]
                    batch = get_batch(features, nextMoves, BATCH_SIZE)
                    i+=1

                    print("%d batches ran. Remaining Feature Length is %d" % (network.get_global_step(), len(features)))

                network.average_summary()    
    
    print("%d batches ran." % i)

    print("Finished in %f secs." % (time.time() - start_time))
    print("Done.")
