# Movidius Neural Compute Stick Instructions
Instructions for deploying a trained model for inference on a Movidius Neural Compute Stick

## Requirements

- Ubuntu 16.04.4
- Python 2.7.12
- pip 8.1+
- six
- numpy
- Matching Tensorflow version to the one that the network was trained on
  - Source files
  - Installed on system
- Bazel 0.10.0 or 0.11.0 https://github.com/bazelbuild/bazel/releases

## Setup

1. Install the NCSDK as per instructions https://github.com/movidius/ncsdk
```
git clone -b ncsdk2 https://github.com/movidius/ncsdk.git
```
2. Freeze a GraphDef from trained checkpoint files
```
bazel build tensorflow/python/tools:freeze_graph && bazel-bin/tensorflow/python/tools/freeze_graph --input_graph="/home/andrew/Downloads/CycleGAN Checkpoints/s2w/graph.pb" --input_checkpoint="/home/andrew/Downloads/CycleGAN Checkpoints/s2w/Epoch_(199)_(562of962).ckpt" --output_graph=/tmp/frozen_graph.pb --output_node_names=a2b_generator/output_image
```

3. Transform a frozen GraphDef using the transform_graph tool
```
bazel build --config=opt tensorflow/tools/graph_transforms:transform_graph && bazel-bin/tensorflow/tools/graph_transforms/transform_graph --in_graph=/tmp/frozen_graph.pb --out_graph=/tmp/movidius_graph.pb --inputs=‘inputA’ --outputs='a2b_generator/output_image' --transforms=' strip_unused_nodes(type=float, shape="1,256,256,3") remove_nodes(op=Identity, op=CheckNumerics) add_default_attributes fold_constants(ignore_errors=true) fold_batch_norms merge_duplicate_nodes'
```
4. Convert the inference optimised graph to a movidius graph format
```
mvNCCompile /tmp/movidius_graph.pb -in inputA -on a2b_generator/output_image
```
