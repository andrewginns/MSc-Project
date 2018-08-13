# Visualising Graphs
Allows a visualisation of the computational graphs. Can serve to highlight differences between models or idenitify specific nodes(ops).

## Requirements
- Tested on macOS 10.13 and Ubuntu 16.04.4
- Python 2.7.12
- pip 8.1+
- six
- numpy
- graphviz
- Tensorflow 1.8+ source files
- Bazel 0.10.0 or 0.11.0 https://github.com/bazelbuild/bazel/releases

## List nodes in GraphDef (.pb) files
In the CycleGAN directory
```
python list_nodes_from_pb.py /path/to/grafdef.pb
```

## View a GraphDef (.pb) in Tensorboard
In the CycleGAN directory
```
python pb_view_tensorboard.py --graph=/home/andrew/Downloads/apple2orange.pb

tensorboard --logdir=/tmp/tensorboard
```

## Visualising GraphDef (.pb) files
### Create a GraphViz-Dot output
Tensorflow 1.6+
```
bazel run --config=opt \
  //tensorflow/contrib/lite/toco:toco -- \
  --input_file=frozen_graph.pb \
  --output_file=foo.dot \
  --input_format=TENSORFLOW_GRAPHDEF \
  --output_format=GRAPHVIZ_DOT \
  --input_shape=1,256,256,3 \
  --input_array=inputA \
  --output_array=a2b_generator/output_image
```
Tensorflow 1.9+
```
bazel run //tensorflow/contrib/lite/python:tflite_convert \
  --graph_def_file=frozen_graph.pb \
  --output_file=foo.dot \
  --output_format=GRAPHVIZ_DOT \
  --input_shape=1,256,256,3 \
  --input_arrays=inputA \
  --output_array=a2b_generator/output_image
```

### Render to an SVG
Inputting the foo.dot file to produce a foo.svg output
```
dot -Tsvg -O foo.dot > foo.svg
```

## Visualising TFLite (.tflite) files
### Build the visualiser
```
bazel build tensorflow/contrib/lite/tools:visualize
```

### Convert the graph to a html output
```
bazel-bin/tensorflow/contrib/lite/tools/visualize foo.tflite foo.html
```
