# Step-by-Step Instructions

## Requirements for reproduction
* Tested on macOS 10.13 and Ubuntu 16.04.4
* Python 2.7.12
* Bazel 0.10.1 https://github.com/bazelbuild/bazel/releases/tag/0.10.1
* Tensorflow 1.6 installed (GPU recommended for training)
* Tensoflow 1.6 source files - For bazel builds
* Tensoflow 1.8 source files - For bazel builds
* CycleGAN code from https://github.com/andrewginns/CycleGAN-Tensorflow-PyTorch
* Android SDK level 27, Build tools 27.0.3, NDK version 15 for mobile benchmarking
* Movidius Neural Compute Stick(MNCS) - For MNCS inference
  * Movidius Neural Compute SDK 2.04.00 https://github.com/movidius/ncsdk/releases
  
## Building Tensorflow (Not mandatory)
Tensorflow only needs to be built from source if you want to customise the use of AVX, AVX2 and FMA instructions. Tested on Ubuntu 16.04.4 and macOS 10.13
  * Building from source can enable significant speedup compared to using an official pre-built .whl
  * The official pre-built .whl files for Tensorflow 1.6+ have AVX enabled by default. Older CPUs may need .whl packages built from source without AVX
  * These instructions are only for the CPU builds
  * My custom pre-built files https://github.com/andrewginns/tflow-whls
    * Includes Tensorflow 1.6 without AVX
    
### Requires a working bazel install (Tested on bazel 0.10.1 and 0.11.0)
  
Tensorflow 1.6
~~~~
git clone https://github.com/tensorflow/tensorflow/releases/tag/v1.6.0

cd tensorflow-1.6.0/
~~~~
Tensoflow 1.8
~~~~
git clone https://github.com/tensorflow/tensorflow/releases/tag/v1.8.0

cd tensorflow-1.8.0/
~~~~
Once your desired source files are downloaded and the directory has been navigated to run
~~~~
./configure
~~~~
This will start an interactive configuration
  * You will likely be using the defaul python paths
  * Enter '-march=native' for the appropriate optimisation flags for the computer you are building on
  * The other options should all be answered no for a default CPU configuration
  
Now you need to build and export the pip package that you will install
~~~~
bazel build --config=opt //tensorflow/tools/pip_package:build_pip_package

bazel-bin/tensorflow/tools/pip_package/build_pip_package /path/to/the/built/.whl
~~~~

This .whl can now be used with pip to install your custom Tensorflow install
~~~~
sudo pip install /path/to/the/built/.whl/tensorflow-1.x.x-py2-none-any.whl
~~~~

  
## Building the Tensorflow tools
These tools are seperate to compiling the main Tensorflow library from source

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

cd tensorflow-1.8.0/

./configure with -march=native, SDK level 27, Build tools 27.0.3, NDK version 15

bazel build --config=opt tensorflow/contrib/lite/toco:toco

bazel build --config=monolithic --cxxopt=--std=c++11 //tensorflow/tools/benchmark:benchmark_model --config=android_arm64 --cpu=arm64-v8a

// All combined
bazel build --config=opt tensorflow/contrib/lite/toco:toco && bazel build --config=monolithic --cxxopt=--std=c++11 //tensorflow/tools/benchmark:benchmark_model --config=android_arm64 --cpu=arm64-v8a
~~~~

## Training and optimizing network
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

## Benchmarking network
Lists all the ops and checks that the graph runs

  1. Desktop benchmarking
~~~~
bazel-bin/tensorflow/tools/benchmark/benchmark_model --graph=/Users/andrewginns/Desktop/vBox/CycleGAN-Tensorflow-PyTorch/outputs/checkpoints/summer2winter_yosemite/optimized_graph.pb --show_sizes=false --show_flops=true --input_layer=inputA --input_layer_type=float --input_layer_shape="1,256,256,3" --output_layer=a2b_generator/output_image
~~~~

  2. Mobile benchmarking

~~~~
adb push bazel-bin/tensorflow/tools/benchmark/benchmark_model /data/local/tmp

adb push /Users/andrewginns/Desktop/vBox/CycleGAN-Tensorflow-PyTorch/outputs/checkpoints/summer2winter_yosemite/quant_optimized_graph.pb /data/local/tmp/

adb shell "/data/local/tmp/benchmark_model --graph=/data/local/tmp/quant_optimized_graph.pb --show_sizes=false --show_flops=true --input_layer=inputA --input_layer_type=float --input_layer_shape="1,256,256,3" --output_layer=a2b_generator/output_image"
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
  Remove bazel - Linux
~~~~
rm -rf ~/.bazel ~/.bazelrc ~/.cache/bazel
~~~~  
  Remove bazel - macOS
~~~~  
rm -rf /usr/local/bin/bazel /usr/local/bin/bazel /usr/local/lib/bazel
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
