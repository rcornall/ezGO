'''
network.py - neural network class

Convolutional Neural Net with 10 layers

Design loosely follows alpha go policy network 
first a 5x5 Conv
followed by 9 3x3 layers using ReLu
'''
import os, sys
import math
import numpy as np

import tensorflow as tf

DIRECTORY = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIRECTORY, '..'))

from defines import Defines as defs

NUMBER_OF_FEATURES = 3
FILTERS = 128


def conv_layer(x, shape, name):
    dimenX = shape[0]
    dimenY = shape[1]
    noInputsFeatures = shape[2]
    noOutputFeatures = shape[3]

    # weight initialization with a zero mean gaussian dist. 
    # with a standard deviation of root(2/ni) , where ni is the 'flattened' size of input vectors
    # this initialization helps deep CNNs (>8 layers) to converge
    # Ref: https://arxiv.org/pdf/1502.01852.pdf
    #  eg for 5x5 conv: root(2/  5    x    5   x input size)
    numberOfInputs = dimenX*dimenY*noInputsFeatures
    stddev = math.sqrt(2/numberOfInputs)
    # print(stddev)

    weights = tf.Variable(tf.truncated_normal(shape, stddev=stddev), name=name+'_weights')

    # bias starts at 0, and need 1 for every output feature
    bias = tf.Variable(tf.constant(0.0, shape=[defs.BOARD_SIZE, defs.BOARD_SIZE, noOutputFeatures],
        name=name+'_biases'))
    return tf.nn.conv2d(x, weights, strides=[1,1,1,1], padding='SAME') + bias

class Network:
    def __init__(self):
        self.session = tf.Session()
        self.training_stats = Collect_stats()
        # x is inputs, y_ is answers
        self.x = tf.placeholder(tf.float32, shape=[None, defs.BOARD_SIZE, defs.BOARD_SIZE, NUMBER_OF_FEATURES])
        self.y_ = tf.placeholder(tf.float64, shape=[None, defs.BOARD_SIZE**2])

        layer1 = tf.nn.relu(conv_layer(self.x, [5, 5, NUMBER_OF_FEATURES, FILTERS], 'conv_1'))
        layer2 = tf.nn.relu(conv_layer(layer1, [3, 3, FILTERS, FILTERS], 'conv_2'))
        layer3 = tf.nn.relu(conv_layer(layer2, [3, 3, FILTERS, FILTERS], 'conv_3'))
        layer4 = tf.nn.relu(conv_layer(layer3, [3, 3, FILTERS, FILTERS], 'conv_4'))
        layer5 = tf.nn.relu(conv_layer(layer4, [3, 3, FILTERS, FILTERS], 'conv_5'))
        layer6 = tf.nn.relu(conv_layer(layer5, [3, 3, FILTERS, FILTERS], 'conv_6'))
        layer7 = tf.nn.relu(conv_layer(layer6, [3, 3, FILTERS, FILTERS], 'conv_7'))
        layer8 = tf.nn.relu(conv_layer(layer7, [3, 3, FILTERS, FILTERS], 'conv_8'))
        layer9 = tf.nn.relu(conv_layer(layer8, [3, 3, FILTERS, FILTERS], 'conv_9'))
        # final layer goes from FILTERS inputs to 1 output (AKA 1 go board)
        layer10 = conv_layer(layer9, [1, 1, FILTERS, 1], 'conv_10_final')
        # final output is flattened to a 1D vector of size 19x19 
        # 1 output logit for every board position
        self.logits = tf.reshape(layer10, [-1, defs.BOARD_SIZE*defs.BOARD_SIZE])

        # softmax converts logits to the normal probability range [0,1]
        self.board_output = tf.nn.softmax(self.logits)
 
        # Loss function is cross entropy btwn target and softmax activation function
        # https://www.tensorflow.org/get_started/mnist/pros
        self.cross_entropy = tf.reduce_mean(
            tf.nn.softmax_cross_entropy_with_logits(logits=self.logits, labels=self.y_))

        # Decaying the learning rate as training progresses
        # https://www.tensorflow.org/versions/r0.12/api_docs/python/train/decaying_the_learning_rate
        self.global_step = tf.Variable(0, trainable=False)
        starter_learning_rate = 0.01
        decayed_learning_rate = tf.train.exponential_decay(starter_learning_rate, self.global_step,
                1000000, 0.96, staircase=True)


        # Using gradient descent to 'descend' the cross entropy, or minimize loss
        # passing in global_step to compute the decayed learning rate
        self.train_step = tf.train.GradientDescentOptimizer(decayed_learning_rate).minimize(self.cross_entropy, global_step=self.global_step)

        # Evaluation functions for our model to see how it does
        # https://www.tensorflow.org/versions/master/get_started/mnist/beginners
        self.is_equal = tf.equal(tf.argmax(self.logits, 1), tf.argmax(self.y_, 1))
        self.accuracy = tf.reduce_mean(tf.cast(self.is_equal, tf.float32))

        self.saver = tf.train.Saver()

        self.session.run(tf.global_variables_initializer())

    def get_global_step(self):
        return self.session.run(self.global_step)
        
    def train(self, batch):
        # train a batch
        print("training a batch...")
        _, loss, accuracy = self.session.run([self.train_step, self.cross_entropy, self.accuracy], 
                feed_dict={self.x: batch['features'].astype(np.float32), self.y_: batch['next_moves'].astype(np.float)})

        #calculate accuracy
        self.training_stats.report(accuracy, loss)

        return

    def average_summary(self):
        avg_accuracy, avg_cost, accuracy_summaries = self.training_stats.collect()
        global_step = self.get_global_step()
        print("Step %d training data accuracy: %g; cost: %g" % (global_step, avg_accuracy, avg_cost))

    
    def test(self, batch):
        loss, accuracy = self.session.run([self.cross_entropy, self.accuracy], 
                feed_dict={self.x: batch['features'].astype(np.float32), self.y_: batch['next_moves'].astype(np.float)})

    def save_checkpoint(self, checkpoint_directory, step):
        print("saving checkpoint %d .." % step)
        self.saver.save(self.session, "%s/checkpoint_%d" % (checkpoint_directory, step))

    def load_checkpoint(self, checkpoint_directory):
        self.saver.restore(self.session, checkpoint_directory)
        print("Loaded checkpoint: %s" % checkpoint_directory)

    def generate_move(self, features):
        print("Generating moves...")
        logits = self.session.run(self.logits, feed_dict={self.x: features})

        # some reason logits is list of 1 array
        print(logits.argmax())
        coordinate = logits.argmax()

        x = int(coordinate/(defs.BOARD_SIZE))
        y = int(coordinate%(defs.BOARD_SIZE))

        print("coords pair")
        print(x,y)
        return x,y


class Collect_stats(object):
    graph = tf.Graph()
    with tf.device("/cpu:0"), graph.as_default():
        accuracy = tf.placeholder(tf.float32, [])
        cost = tf.placeholder(tf.float32, [])
        accuracy_summary = tf.summary.scalar("accuracy", accuracy)
        cost_summary = tf.summary.scalar("cross_entropy", cost)
        accuracy_summaries = tf.summary.merge([accuracy_summary, cost_summary], name="accuracy_summaries")
    session = tf.Session(graph=graph)
    
    def __init__(self):
        self.accuracies = []
        self.costs = []

    def report(self, accuracy, cost):
        self.accuracies.append(accuracy)
        self.costs.append(cost)

    def collect(self):
        print(self.accuracies)
        avg_acc = sum(self.accuracies) / len(self.accuracies)
        avg_cost = sum(self.costs) / len(self.costs)
        self.accuracies = []
        self.costs = []
        summary = self.session.run(self.accuracy_summaries,
            feed_dict={self.accuracy:avg_acc, self.cost: avg_cost})
        return avg_acc, avg_cost, summary
