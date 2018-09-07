# Model Optimisation Instructions

Model optimisation turns a trained frozen_graph.pb into various optimised models in different formats (.pb .tflite). These optimisations prepare the model for inference by removing and transforming operations to reduce size and increase speed.

## Requirements

- Tested on macOS 10.13 and Ubuntu 16.04.4
- Python 2.7.12
- pip 8.1+
- six
- numpy
- Tensorflow 1.6 source files
- Tensorflow 1.8+ source files source files with a configured WORKSPACE
- Bazel 0.10.0 or 0.11.0 https://github.com/bazelbuild/bazel/releases
- Android Studio: Android SDK level 27, Build tools 27.0.3, NDK version 15

## GraphDef (.pb)

Optimise the model GraphDef for inference using TF1.6 tools

1. Floating point model (optimized-graph.pb)

```
bazel build --config=opt tensorflow/tools/graph_transforms:transform_graph && bazel-bin/tensorflow/tools/graph_transforms/transform_graph --in_graph=/tmp/frozen-graph.pb --out_graph=/tmp/optimized-graph.pb --inputs=‘inputA’ --outputs='a2b_generator/output_image' --transforms='add_default_attributes fold_constants(ignore_errors=true) fold_batch_norms quantize_weights merge_duplicate_nodes sort_by_execution_order'
```

2. Quantised model (quant_quant.pb)

```
bazel build --config=opt tensorflow/tools/graph_transforms:transform_graph && bazel-bin/tensorflow/tools/graph_transforms/transform_graph --in_graph=/tmp/frozen-graph.pb --out_graph=/tmp/optimized-graph.pb --inputs=‘inputA’ --outputs='a2b_generator/output_image' --transforms='add_default_attributes fold_constants(ignore_errors=true) fold_batch_norms quantize_weights quantize_nodes sort_by_execution_order'
```

## TFLite (.tflite)

Convert to an optimised TFLite model for Android inference using TF1.8+ tools

1. Floating point model (float.tflite)

```
tflite_convert \
  --output_file=/tmp/foo.tflite \
  --graph_def_file=/home/andrew/Downloads/frozen-graph.pb \
  --input_arrays=inputA \
  --output_arrays=a2b_generator/output_image
```

2. Quantised model 

```
//Fake quant - Fails due to lack of support for de-convolution
tflite_convert \
  --output_file=/tmp/foo.tflite \
  --graph_def_file=/home/andrew/Downloads/frozen-graph.pb \
  --inference_type=QUANTIZED_UINT8 \
  --input_arrays=inputA \
  --output_arrays=a2b_generator/output_image \
  --default_ranges_min=0 \
  --default_ranges_max=6 \
  --mean_values=128 \
  --std_dev_values=127
```
