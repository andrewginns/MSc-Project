# Model Optimisation Instructions

Model optimisations turn a trained frozen_graph.pb into various optimised models in different formats (.pb .tflite). These optimisations prepare the model for inference by removing and transforming operations to reduce size and increase speed.

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

1. Floating point model

```
bazel build --config=opt tensorflow/tools/graph_transforms:transform_graph && bazel-bin/tensorflow/tools/graph_transforms/transform_graph --in_graph=/Users/andrewginns/Desktop/vBox/frozen_graph.pb --out_graph=/Users/andrewginns/Desktop/vBox/optimized_graph.pb --inputs=‘inputA’ --outputs='a2b_generator/output_image' --transforms=' strip_unused_nodes(type=float, shape="1,256,256,3") remove_nodes(op=Identity, op=CheckNumerics) fold_batch_norms'
```

2. Quantised model

```
bazel build --config=opt tensorflow/tools/graph_transforms:transform_graph && bazel-bin/tensorflow/tools/graph_transforms/transform_graph --in_graph=/Users/andrewginns/Desktop/vBox/frozen_graph.pb --out_graph=/Users/andrewginns/Desktop/vBox/2-quant-optimized_graph.pb --inputs=‘inputA’ --outputs='a2b_generator/output_image' --transforms=' strip_unused_nodes(type=float, shape="1,256,256,3") remove_nodes(op=Identity, op=CheckNumerics) fold_batch_norms quantize_weights strip_unused_nodes sort_by_execution_order '
```

## TFLite (.tflite)

Convert to an optimised TFLite model for Android inference using TF1.8+ tools

1. Floating point model

```
tflite_convert \
--output_file=graph.tflite \
--graph_def_file=frozen_graph.pb \
--input_arrays=inputA \
--output_arrays=a2b_generator/output_image

toco --output_file=toco.tflite \
--graph_def_file=frozen_graph.pb \
--output_format=TFLITE \
--inference_type=FLOAT \
--inference_input_type=FLOAT \
--input_arrays=inputA \
--output_arrays=a2b_generator/output_image
```

2. Quantised model **WIP**

```
tflite_convert \
--output_file=graph-fakequant.tflite \
--graph_def_file=2-quant-optimized_graph.pb \
--inference_type=QUANTIZED_UINT8 \
--input_arrays=inputA \
--output_arrays=a2b_generator/output_image \
--default_ranges_min=0 \
--default_ranges_max=6 \
--mean_values=128 \
--std_dev_values=127

toco --output_file=toco-quant.tflite \
--graph_def_file=frozen_graph.pb \
--output_format=TFLITE \
--inference_type=QUANTIZED_UINT8 \
--inference_input_type=QUANTIZED_UINT8 \
--input_arrays=inputA \
--output_arrays=a2b_generator/output_image \
--std_dev_values=127 \
--mean_values=128 \
--default_ranges_min=0 \
--default_ranges_max=6 \
--quantize_weights QUANTIZE_WEIGHTS
```
