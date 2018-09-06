from __future__ import absolute_import, division, print_function

import argparse
import models
import tensorflow as tf
import utils
from functools import partial

""" param """
parser = argparse.ArgumentParser(description='')
parser.add_argument('--checkpoints', dest='checkpoints', default='C:/Users/ginns/Desktop/CycleGAN-Tensorflow-PyTorch/outputs/checkpoints/norm2pro_256',
                    help='path of model checkpoint files')
args = parser.parse_args()

checkpoints = args.checkpoints
crop_size = 100

""" run """
with tf.Session() as sess:
    # Define the graph inputs
    a_input = tf.placeholder(tf.float32, shape=[None, crop_size, crop_size, 3])

    # Define the placeholder values
    a_real = tf.placeholder(tf.float32, shape=[None, crop_size, crop_size, 3], name="inputA")
    # b_real = tf.placeholder(tf.float32, shape=[None, crop_size, crop_size, 3], name="inputB")
    # a2b_sample = tf.placeholder(tf.float32, shape=[None, crop_size, crop_size, 3])
    # b2a_sample = tf.placeholder(tf.float32, shape=[None, crop_size, crop_size, 3])

    # Define what parts of the graph to evaluate

    # Generator and Discriminator
    generator_a2b = partial(models.generator, scope='a2b')
    # generator_b2a = partial(models.generator, scope='b2a')
    # discriminator_a = partial(models.discriminator, scope='a')
    # discriminator_b = partial(models.discriminator, scope='b')

    # Forward and backward passes
    a2b = generator_a2b(a_real)
    # b2a = generator_b2a(b_real)
    # b2a2b = generator_a2b(b2a)
    # a2b2a = generator_b2a(a2b)

    # Input values
    # a_logit = discriminator_a(a_real)
    # b2a_logit = discriminator_a(b2a)
    # b2a_sample_logit = discriminator_a(b2a_sample)
    # b_logit = discriminator_b(b_real)
    # a2b_logit = discriminator_b(a2b)
    # a2b_sample_logit = discriminator_b(a2b_sample)

    # Restore weights
    try:
        ckpt_path = utils.load_checkpoint(checkpoints, sess)
    except IOError as e:
        raise Exception('No checkpoint found!')

    # Count parameters
    total_parameters = 0
    for variable in tf.trainable_variables():
        # shape is an array of tf.Dimension
        shape = variable.get_shape()
        print(shape)
        print(len(shape))
        variable_parameters = 1
        for dim in shape:
            print(dim)
            variable_parameters *= dim.value
        print(variable_parameters)
        total_parameters += variable_parameters

    n = len([n.name for n in tf.get_default_graph().as_graph_def().node])
    print("No.of nodes: ", n, "\n")

    print("\nTotal parameters:\n", total_parameters)

    print(str((total_parameters*4)/1e6) + "MB")
