# Model Optimisation
Taking a trained model and turning it into one ready for inference involves several steps and a multitude of choices. This will outline theses steps along with the important choices and their impact.

## Freezing a graph
During the training step Tensorflow stores the weights of the network seperate from the structure of the network. The structure is made up of *Variable* ops that load the stored values when initialised.

The first task it to take these seperate .ckpt files and combine them into a single file.

This single file is called a GrafDef file in the .pb format. In addition to merging the various files the GrafDef also replaces each of the *Variable* ops with a *Const* that fixes the weights of the network.

This step is also where the model's input and output nodes are definined. In this case the GAN contains two different convolutional networks; a generator and a discriminator. For the purpose of style-transfer only the generator is required. The input node is therefore defined as the input to the generator network and the output node is defined as the output from the generator network. These are called 'inputA' and 'a2b_generator/output_image' respectively.

In this project this output graph is called frozen_graph.pb containing 625 ops

The command for doing this is step 3 and 4 in https://github.com/andrewginns/MSc-Project/blob/master/Training_Instructions.md

## Transforming the graph
To make models run more efficiently the GrafDef can be further transformed. This is doen through a the Graph Transform Tool that can re-write the GrafDef with several user defined actions. The following command is used to produce the optimized-graph.pb
```
bazel build --config=opt tensorflow/tools/graph_transforms:transform_graph && bazel-bin/tensorflow/tools/graph_transforms/transform_graph --in_graph=/tmp/frozen-graph.pb --out_graph=/tmp/optimized-graph.pb --inputs=‘inputA’ --outputs='a2b_generator/output_image' --transforms='add_default_attributes fold_constants(ignore_errors=true) fold_batch_norms quantize_weights merge_duplicate_nodes sort_by_execution_order'
```

Arguments are passed to the '--transform' option. Detail about each of these options and the effect is has on the final graph is described below.

The aim of these tools is to shrink file size and in some cases speed up computation. This is particularly important in mobile applications where it helps reduce application size.

Reference from official docs here: https://github.com/tensorflow/tensorflow/blob/master/tensorflow/tools/graph_transforms/README.md#fold_constants

### add_default_attributes
Allows the model to be processed correctly outside of a main Tensorflow framework. It adds in a any op attributes not defined in the saved model.

### fold_constants(ignore_errors=true)
Replaces any sub-graphs that always evaluate to constants with those constants. 'ignore_error=true' ignores any transient errors that can occur during the transform.

### fold_batchnorms
Removes the 'Mul' operation that comes after a 'Conv2D' operation during batch nomalisation. Replaces the multiplations after these convolutions with just the contants. (Requires that fold_constants is run beforehand)

### quantized_weights
Converts any 'Const' operations with more than 1024 elements to an 8-bit equivalent. This helps dramatically shrink file size, in this model this transform brings size down from 45.9MB to 11.8MB.

### merge_duplicate_nodes
Merges any 'Const' nodes with the same types and values, or nodes with the same inputs and attributes.

### sort_by_execution_order
Sorts the nodes in the GraphDef to be in the order of execution. This means all inputs are computed before they are needed. This helps achieve minimal inference as the node can be executed in the order that they are presented.
