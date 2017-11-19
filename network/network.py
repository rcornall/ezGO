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
    def __init__(self, num_conv_layers = 11):
        # Setup the network weights and layers here
        self.num_conv_layers = num_conv_layers
        return

    def network_set_up(self):
        global_step = tf.Variable(0, name="global_step", trainable=False)
        RL_global_step = tf.Variable(0, name="RL_global_step", trainable=False)
        x = tf.placeholder(tf.float32, [None, go.N, go.N, self.num_input_planes])
        y = tf.placeholder(tf.float32, shape=[None, go.N ** 2])

        #convenience functions for initializing weights and biases
        def _weight_variable(shape, name):
            # If shape is [5, 5, 20, 32], then each of the 32 output planes
            # has 5 * 5 * 20 inputs.
            number_inputs_added = utils.product(shape[:-1])
            stddev = 1 / math.sqrt(number_inputs_added)
            # http://neuralnetworksanddeeplearning.com/chap3.html#weight_initialization
            return tf.Variable(tf.truncated_normal(shape, stddev=stddev), name=name)

        def _conv2d(x, W):
            return tf.nn.conv2d(x, W, strides=[1,1,1,1], padding="SAME")

    def train(self, batch):
        # train a batch
        return
