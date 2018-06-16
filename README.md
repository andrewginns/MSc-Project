# MSc-Project
Repo for MSc Advanced Project for the degree of Advanced Computing at the University of Bristol

### Core code https://github.com/andrewginns/CycleGAN-Tensorflow-PyTorch
### Files https://github.com/andrewginns/CycleGAN-Tensorflow-PyTorch/releases

## Instructions for use: https://github.com/andrewginns/MSc-Project/blob/master/instructions.md

## Current problems https://github.com/andrewginns/MSc-Project/blob/master/Current_Problems.md

# Requirements for reproduction
* Ubuntu 16.04.4
* Movidius Neural Compute Stick
* Movidius Neural Compute SDK 2.04.00 https://github.com/movidius/ncsdk/releases
* Bazel 0.11.0
* Tensorflow 1.6 installed
* Tensoflow 1.6 source files https://github.com/tensorflow/tensorflow/releases/tag/v1.6.0
* Python 2.7.12
* CycleGAN code from https://github.com/andrewginns/CycleGAN-Tensorflow-PyTorch

# Command Reference

Overview of commands used to generate the required outputs

Graph Transform Tools reference
* https://github.com/tensorflow/tensorflow/blob/r1.6/tensorflow/tools/graph_transforms/README.md
* https://www.tensorflow.org/versions/r1.6/mobile/prepare_models

Movidius Reference
* https://movidius.github.io/ncsdk/

TFLite reference
* https://github.com/tensorflow/tensorflow/blob/r1.6/tensorflow/contrib/lite/toco/g3doc/cmdline_examples.md

## Training a model
* git clone https://github.com/andrewginns/CycleGAN-Tensorflow-PyTorch

* cd CycleGAN-Tensorflow-PyTorch

* chmod +x ./download_dataset.sh

* ./download_dataset.sh summer2winter_yosemite

* CUDA_VISIBLE_DEVICES=0 python train.py --dataset=horse2zebra

## Building the tools
* git clone https://github.com/tensorflow/tensorflow/releases/tag/v1.6.0

* cd tensorflow-1.6.0

* ./configure with -march=native

* bazel build --config=opt tensorflow/tools/graph_transforms:summarize_graph

* bazel build --config=opt tensorflow/python/tools:freeze_graph

* bazel build --config=opt tensorflow/tools/benchmark:benchmark_model

* bazel build --config=opt tensorflow/tools/graph_transforms:transform_graph

* bazel build --config=opt tensorflow/contrib/lite/toco:toco

All-in-one
*bazel build --config=opt tensorflow/tools/graph_transforms:summarize_graph && bazel build --config=opt tensorflow/python/tools:freeze_graph && bazel build --config=opt tensorflow/tools/benchmark:benchmark_model && bazel build --config=opt tensorflow/tools/graph_transforms:transform_graph && bazel build --config=opt tensorflow/contrib/lite/toco:toco*

## Using the tools

### Summarize GrafDef proto to view nodes and other info

* Copy the graph.pb from outputs/checkpoints/dataset to tensorflow-1.6.0 folder
* bazel-bin/tensorflow/tools/graph_transforms/summarize_graph --in_graph=graph.pb
* Note the input and output nodes

### Freeze the graph by combining the GrafDef proto and the checkpoints

* cd CycleGAN-Tensorflow-PyTorch
* Copy checkpoint, and all .ckpt files to directory
* python freeze.py

### View the graph in Tensorboard

* tensorboard --logdir=logs/ --host localhost --port 8088

### Summarize the GraphDef to view nodes and other info, should be reduced compared to the graph.pb

* bazel-bin/tensorflow/tools/graph_transforms/summarize_graph --in_graph=/tmp/frozen_graph.pb

### Benchmark the unoptimised model

* bazel-bin/tensorflow/tools/benchmark/benchmark_model --graph=/Users/andrewginns/Desktop/vBox/frozen_graph.pb --show_sizes=false --show_flops=true --input_layer=inputA --input_layer_type=float --input_layer_shape="1,256,256,3" --output_layer=a2b_generator/output_image

### Optimise the model

* bazel-bin/tensorflow/tools/graph_transforms/transform_graph --in_graph=/Users/andrewginns/Desktop/vBox/frozen_graph.pb --out_graph=/Users/andrewginns/Desktop/vBox/optimized_graph.pb --inputs=‘inputA’ --outputs='a2b_generator/output_image' --transforms=' strip_unused_nodes(type=float, shape="1,256,256,3") remove_nodes(op=Identity, op=CheckNumerics) fold_batch_norms'
 
### Benchmark the optimised model

* bazel-bin/tensorflow/tools/benchmark/benchmark_model --graph=/Users/andrewginns/Desktop/vBox/optimized_graph.pb --show_sizes=false --show_flops=true --input_layer=inputA --input_layer_type=float --input_layer_shape="1,256,256,3" --output_layer=a2b_generator/output_image

## Desktop inference
* Using the checkpoint files (.ckpt)
    * python test.py --dataset=one_of_the_datasets
        * Output images are from left to right: original image --> a2b --> b2a
    * python ckpt_a2b.py --checkpoints='/path/to/checkpoints.ckpt' --dataset='/path/to/images.jpg'
        * Output images are from left to right: original image --> a2b
        
* Using a model file (.pb)
    * python pb_a2b.py --graph='/path/to/.pb' --dataset='/path/to/images.jpg'
        * Output images are from left to right: original image --> a2b

## Convert the model to an Intel Movidius graph

* cd ~/

* mvNCCompile /media/sf_vBox/optimized_graph.pb -in inputA -on a2b_generator/output_image


## Convert the model to a TFLite model

* cd tensorflow-1.8
  
* bazel-bin/tensorflow/contrib/lite/toco/toco \
    --input_file=/Users/andrewginns/Desktop/vBox/optimized_graph.pb \
    --output_file=/Users/andrewginns/Desktop/vBox/graph.lite \
    --input_format=TENSORFLOW_GRAPHDEF \
    --output_format=TFLITE \
    --input_shape=1,256,256,3 \
    --input_array=inputA \
  
## Useful commands
Remove bazel
* rm -fr ~/.bazel ~/.bazelrc ~/.cache/bazel

Install bazel
* sudo apt-get install pkg-config zip g++ zlib1g-dev unzip python
* wget https://github.com/bazelbuild/bazel/releases/download/0.11.0/bazel-0.11.0-installer-linux-x86_64.sh
* chmod +x bazel-0.11.0-installer-linux-x86_64.sh
* ./bazel-0.11.0-installer-linux-x86_64.sh --user
* export PATH="$PATH:$HOME/bin"
