# Step-by-Step Instructions

## Requirements for reproduction
* Tested on macOS 10.13 and Ubuntu 16.04.4
* Python 2.7.12
* Bazel 0.11.0
  * https://github.com/bazelbuild/bazel/releases/tag/0.11.0
* Tensorflow 1.6 installed (GPU recommended for training)
  * Tensoflow 1.6 source files https://github.com/tensorflow/tensorflow/releases/tag/v1.6.0
* CycleGAN code from https://github.com/andrewginns/CycleGAN-Tensorflow-PyTorch
* Tensoflow 1.8 source files - For TFLite inference
* Movidius Neural Compute Stick(MNCS) - For MNCS inference
  * Movidius Neural Compute SDK 2.04.00 https://github.com/movidius/ncsdk/releases
  
## Building the tools
  1. Tensorflow 1.6
~~~~
git clone https://github.com/tensorflow/tensorflow/releases/tag/v1.6.0

cd tensorflow-1.6.0/

./configure with -march=native

bazel build --config=opt tensorflow/tools/graph_transforms:summarize_graph

bazel build --config=opt tensorflow/python/tools:freeze_graph

bazel build --config=opt tensorflow/tools/benchmark:benchmark_model

bazel build --config=opt tensorflow/tools/graph_transforms:transform_graph

// All combined
bazel build --config=opt tensorflow/tools/graph_transforms:summarize_graph && bazel build --config=opt tensorflow/python/tools:freeze_graph && bazel build --config=opt tensorflow/tools/benchmark:benchmark_model && bazel build --config=opt tensorflow/tools/graph_transforms:transform_graph
~~~~
  2. Tensoflow 1.8
~~~~
git clone https://github.com/tensorflow/tensorflow/releases/tag/v1.8.0

cd tensorflow-1.6.0/

bazel build --config=opt tensorflow/contrib/lite/toco:toco
~~~~

## Training the network
  1. Navigate to the directory and download training sets
~~~~
cd $HOME/path/to/CycleGAN-Tensorflow-PyTorch

chmod +x ./download_dataset.sh

./download_dataset.sh summer2winter_yosemite
~~~~
  2. Run the network training - CUDA_VISIBLE_DEVICES=0 can be used to specify the GPU ID to use
~~~~
python train.py --dataset=summer2winter_yosemite
~~~~
  3. Collect the output files from outputs/checkpoints/dataset and outputs/summaries/dataset
  4. Freeze the network into a graph file
~~~~
python freeze.py --checkpoint_path=./outputs/checkpoints/dataset --output_nodes=a2b_generator/output_image --output_graph=/tmp/frozen-graph.pb
~~~~
  5. Optimize the graph
~~~~
bazel-bin/tensorflow/tools/graph_transforms/transform_graph --in_graph=/Users/andrewginns/Desktop/vBox/frozen_graph.pb --out_graph=/Users/andrewginns/Desktop/vBox/optimized_graph.pb --inputs=‘inputA’ --outputs='a2b_generator/output_image' --transforms=' strip_unused_nodes(type=float, shape="1,256,256,3") remove_nodes(op=Identity, op=CheckNumerics) fold_batch_norms'
~~~~
  6. Benchmark the graphs - Lists all the ops and checks that the graph runs
~~~~
bazel-bin/tensorflow/tools/benchmark/benchmark_model --graph=/Users/andrewginns/Desktop/vBox/optimized_graph.pb --show_sizes=false --show_flops=true --input_layer=inputA --input_layer_type=float --input_layer_shape="1,256,256,3" --output_layer=a2b_generator/output_image
~~~~

## Desktop inference
Option 1: Using the checkpoint files (.ckpt)
~~~~
python test.py --dataset=one_of_the_datasets
~~~~
  * Output images are from left to right: original image --> a2b --> b2a
~~~~
python ckpt_a2b.py --checkpoints='/path/to/checkpoints.ckpt' --dataset='/path/to/images_folder'
~~~~
  * Output images are from left to right: original image --> a2b

Option 2: Using a model file (.pb)
~~~~
python pb_a2b.py --graph='/path/to/.pb' --dataset='/path/to/image_folder'
~~~~
  * Output images are from left to right: original image --> a2b

## Edge node inference
Targetting:
  * Android Devices with API level 27 (8.1 Oreo) and TF Lite 1.8
  * Movidius Neural Compute Stick with Myriad 2 VPU and SDK 2.04

### Android Devices
Option 1: Use .pb file https://github.com/andrewginns/CycleGAN-TF-Android
  1. Use the .pb graph as is by placing it in CycleGAN-TF-Android/android/assets
  2. Compile the project

Option 2: Convert to an optimised TFLite model
  1. Use TF1.8 tools
~~~~
 bazel-bin/tensorflow/contrib/lite/toco/toco \
--input_file=/Users/andrewginns/Desktop/vBox/optimized_graph.pb \
--output_file=/Users/andrewginns/Desktop/vBox/graph.tflite \
--input_format=TENSORFLOW_GRAPHDEF \
--output_format=TFLITE \
--input_shape=1,256,256,3 \
--input_array=inputA \
~~~~
  2. Add converted graph.tflite to TFLite Android app project
  3. Compile the project

### Movidius Neural Compute Stick
Convert to a Intel Movidius graph format - Ubuntu 16.04.4 required
  1. mvNCCompile /media/sf_vBox/optimized_graph.pb -in inputA -on a2b_generator/output_image
  
## Other tools
  
### Summarize GrafDef proto to view nodes and other info
~~~~
bazel-bin/tensorflow/tools/graph_transforms/summarize_graph --in_graph=path/to/graph.pb
~~~~
  
### View the graph in Tensorboard
~~~~
tensorboard --logdir=logs/ --host localhost --port 8088
~~~~

### Summarize the GraphDef to view nodes and other info, should be reduced compared to the graph.pb
~~~~  
bazel-bin/tensorflow/tools/graph_transforms/summarize_graph --in_graph=/tmp/frozen_graph.pb
~~~~  
  
## Useful commands

### Bazel
  Remove bazel
~~~~
rm -fr ~/.bazel ~/.bazelrc ~/.cache/bazel
~~~~  
  
  Install bazel
~~~~
sudo apt-get install pkg-config zip g++ zlib1g-dev unzip python

wget https://github.com/bazelbuild/bazel/releases/download/0.11.0/bazel-0.11.0-installer-linux-x86_64.sh

chmod +x bazel-0.11.0-installer-linux-x86_64.sh

./bazel-0.11.0-installer-linux-x86_64.sh --user

export PATH="$PATH:$HOME/bin"
~~~~

## Additional Resources

  Tensorflow reference
  * https://www.tensorflow.org/api_docs/
  
  Graph Transform Tools reference
  * https://github.com/tensorflow/tensorflow/blob/r1.6/tensorflow/tools/graph_transforms/README.md
  * https://www.tensorflow.org/versions/r1.6/mobile/prepare_models
  
  Movidius Reference
  * https://movidius.github.io/ncsdk/
  
  TFLite reference
  * https://github.com/tensorflow/tensorflow/blob/r1.6/tensorflow/contrib/lite/toco/g3doc/cmdline_examples.md
