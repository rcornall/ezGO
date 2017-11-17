'''
network.py - neural network class

Convolutional Neural Net with 11 layers

Design loosely follows alpha go policy network 
first a 5x5 Conv
followed by 10 3x3 layers using ReLu
'''
import os, sys

import tensorflow as tf

DIRECTORY = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIRECTORY, '..'))

from defines import Defines as defs



class Network:
    def __init__(self):
        # Setup the network weights and layers here
        return

    def train(self, batch):
        # train a batch
        return
