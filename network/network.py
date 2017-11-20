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
    def __init__(self, k=128, num_conv_layers = 11):
        # Setup the network weights and layers here
        self.num_conv_layers = num_conv_layers
        self.k = k
        return
        


    '''

    go.N and num_input_plane are not defined
   
    '''
    def network_set_up(self):
        global_step = tf.Variable(0, name="global_step", trainable=False)
        RL_global_step = tf.Variable(0, name="RL_global_step", trainable=False)
        x = tf.placeholder(tf.float32, [None, go.N, go.N, self.num_input_planes])
        y = tf.placeholder(tf.float32, shape=[None, go.N ** 2])

        #custom functions for initializing weights and biases
        def _weight_variable(shape, name):
            # If shape is [5, 5, 20, 32], then each of the 32 output planes
            # has 5 * 5 * 20 inputs.
            number_inputs_added = utils.product(shape[:-1])
            stddev = 1 / math.sqrt(number_inputs_added)
            # http://neuralnetworksanddeeplearning.com/chap3.html#weight_initialization
            return tf.Variable(tf.truncated_normal(shape, stddev=stddev), name=name)

        def _conv2d(x, W):
            return tf.nn.conv2d(x, W, strides=[1,1,1,1], padding="SAME")

        #first layer 5x5
        W_conv_init55 = _weight_variable([5, 5, self.num_input_planes, self.k], name="W_conv_init55")
        W_conv_init11 = _weight_variable([1, 1, self.num_input_planes, self.k], name="W_conv_init11")
        h_conv_init = tf.nn.relu(_conv2d(x, W_conv_init55) + _conv2d(x, W_conv_init11), name="h_conv_init")

        # followed by a series of resnet 3x3 conv layers
        W_conv_intermediate = []
        h_conv_intermediate = []
        _current_h_conv = h_conv_init
        for i in range(self.num_int_conv_layers):
            with tf.name_scope("layer"+str(i)):
                _resnet_weights1 = _weight_variable([3, 3, self.k, self.k], name="W_conv_resnet1")
                _resnet_weights2 = _weight_variable([3, 3, self.k, self.k], name="W_conv_resnet2")
                _int_conv = tf.nn.relu(_conv2d(_current_h_conv, _resnet_weights1), name="h_conv_intermediate")
                _output_conv = tf.nn.relu(
                    _current_h_conv +
                    _conv2d(_int_conv, _resnet_weights2),
                    name="h_conv")
                W_conv_intermediate.extend([_resnet_weights1, _resnet_weights2])
                h_conv_intermediate.append(_output_conv)
                _current_h_conv = _output_conv
        
        #final layer
        W_conv_final = _weight_variable([1, 1, self.k, 1], name="W_conv_final")
        b_conv_final = tf.Variable(tf.constant(0, shape=[go.N ** 2], dtype=tf.float32), name="b_conv_final")
        h_conv_final = _conv2d(h_conv_intermediate[-1], W_conv_final)

        #output
        output = tf.nn.softmax(tf.reshape(h_conv_final, [-1, go.N ** 2]) + b_conv_final)
        logits = tf.reshape(h_conv_final, [-1, go.N ** 2]) + b_conv_final

        log_likelihood_cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=y))


    def train(self, batch):
        # train a batch
        return
