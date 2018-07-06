# Tensorflow Tools Build Instructions

These tools are separate to compiling the main Tensorflow library from source

## Requirements

- Tested on macOS 10.13 and Ubuntu 16.04.4
- Python 2.7.12
- pip 8.1+
- six
- numpy
- Bazel 0.10.0 or 0.11.0 https://github.com/bazelbuild/bazel/releases
- Android Studio: Android SDK level 27, Build tools 27.0.3, NDK version 15

## Building the Tools

Separate Tensorflow versions are used for different tools. This is done due to compatibility reasons.

### Tensorflow 1.6

These are tools used for desktop inference and transforming trained models to produce various optimised outputs in the .pb format.

```
git clone https://github.com/tensorflow/tensorflow/releases/tag/v1.6.0

cd tensorflow-1.6.0/

./configure
```

This will start an interactive configuration

- You will likely be using the default python paths
- Enter '-march=native' for the appropriate optimisation flags for the computer you are building on
- The other options should all be answered no for a default CPU configuration

Now build the tools

```
bazel build --config=opt tensorflow/tools/graph_transforms:summarize_graph

bazel build --config=opt tensorflow/python/tools:freeze_graph

bazel build --config=opt tensorflow/tools/benchmark:benchmark_model

bazel build --config=opt tensorflow/tools/graph_transforms:transform_graph

// Build all in a single command
bazel build --config=opt tensorflow/tools/graph_transforms:summarize_graph && bazel build --config=opt tensorflow/python/tools:freeze_graph && bazel build --config=opt tensorflow/tools/benchmark:benchmark_model && bazel build --config=opt tensorflow/tools/graph_transforms:transform_graph
```

### Tensorflow 1.8+

These are tools used for Android inference and transforming trained models to produce various optimised outputs in the .tflite format.

```
git clone https://github.com/tensorflow/tensorflow/releases/tag/v1.8.0

cd tensorflow-1.8.0/

./configure
```

This will start an interactive configuration

- You will likely be using the defaul python paths
- Enter '-march=native' for the appropriate optimisation flags for the computer you are building on
- Choose to configure the interactive WORKSPACE with SDK level 27, Build tools 27.0.3 and NDK version 15
- The other options should all be answered no for a default CPU configuration

Now build the tools

```
bazel build --config=opt tensorflow/contrib/lite/toco:toco

bazel build --config=monolithic --cxxopt=--std=c++11 //tensorflow/tools/benchmark:benchmark_model --config=android_arm64 --cpu=arm64-v8a

bazel build --config=opt tensorflow/contrib/lite/tools/benchmark:benchmark_model

bazel build --config=monolithic --config=android_arm64 --cxxopt='--std=c++11' tensorflow/contrib/lite/tools/benchmark:benchmark_model

// Build all in a single command
bazel build --config=opt tensorflow/contrib/lite/toco:toco && bazel build --config=monolithic --cxxopt=--std=c++11 //tensorflow/tools/benchmark:benchmark_model --config=android_arm64 --cpu=arm64-v8a && bazel build --config=opt tensorflow/contrib/lite/tools/benchmark:benchmark_model && bazel build --config=monolithic --config=android_arm64 --cxxopt='--std=c++11' tensorflow/contrib/lite/tools/benchmark:benchmark_model
```
