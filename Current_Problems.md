#  Current problems
## The problem as well as steps to reproduce and fixes in progress (if any)
    
1. Movidius mvNCCompile gives a compilation error when attempting to convert the graph
~~~~
mvNCCompile /media/sf_vBox/optimized_graph.pb -in inputA -on a2b_generator/output_image
/usr/local/bin/ncsdk/Controllers/Parsers/TensorFlowParser/Convolution.py:44: SyntaxWarning: assertion is always true, perhaps remove parentheses?
assert(False, "Layer type not supported by Convolution: " + obj.type)
mvNCCompile v02.00, Copyright @ Intel Corporation 2017

/usr/local/lib/python3.5/dist-packages/tensorflow/python/util/tf_inspect.py:45: DeprecationWarning: inspect.getargspec() is deprecated, use inspect.signature() instead
shape: [1, 256, 256, 3]
Traceback (most recent call last):
File "/usr/local/bin/mvNCCompile", line 169, in <module>
create_graph(args.network, args.image, args.inputnode, args.outputnode, args.outfile, args.nshaves, args.inputsize, args.weights, args.explicit_concat, args.ma2480, args.scheduler, args.new_parser, args)
File "/usr/local/bin/mvNCCompile", line 148, in create_graph
load_ret = load_network(args, parser, myriad_config)
File "/usr/local/bin/ncsdk/Controllers/Scheduler.py", line 100, in load_network
parse_ret = parse_tensor(arguments, myriad_conf)
File "/usr/local/bin/ncsdk/Controllers/TensorFlowParser.py", line 319, in parse_tensor
item_shape = output_item.shape.as_list()
File "/usr/local/lib/python3.5/dist-packages/tensorflow/python/framework/tensor_shape.py", line 820, in as_list
raise ValueError("as_list() is not defined on an unknown TensorShape.")
ValueError: as_list() is not defined on an unknown TensorShape.
~~~~
  * A dialogue has been opened with Movidius support about this https://ncsforum.movidius.com/discussion/865/conversion-of-frozen-tensorflow-graph-to-movidius-graph#latest


2. The Android app is not showing a live preview of the network output properly
  * This is likely being caused by input to the network being RGB instead of expected jpeg
  * Code to convert from camera YUV420 output to jpeg is being developed
    
    
# Solved

### Solved by writing own freeze graph script
1. The default freeze_graph does not work on CycleGAN due to moving_mean ops
* A custom implementation of freeze.py is implemented instead

### Solved using the TF1.8 tools
2. freeze.py seems to introduce a node called _SOURCE with type 'NoOp' 
    * This is causing problems with the TFLite conversion
~~~~
toco --input_file=/Users/andrewginns/Desktop/vBox/optimized_graph.pb \
    >   --output_file=/Users/andrewginns/Desktop/vBox/graph.lite \
    >   --input_format=TENSORFLOW_GRAPHDEF \
    >   --output_format=TFLITE \
    >    --input_shape=1,256,256,3 \
    >   --input_array=inputA \
    >   --output_array=a2b_generator/output_image
    2018-06-16 14:47:07.775019: F tensorflow/core/graph/graph.cc:283] Non-OK-status: status status: Not found: Op type not registered 'NoOp' in binary running on Andrews-MacBook-Pro.local. Make sure the Op and Kernel are registered in the binary running in this process.
    Abort trap: 6
~~~~
    
3. Investigating problem 2 using summarize_graph seems to give the same output
* Graph frozen with freeze.py
~~~~
bazel-bin/tensorflow/tools/graph_transforms/summarize_graph --in_graph=/Users/andrewginns/Desktop/vBox/frozen_graph.pb
Found 1 possible inputs: (name=inputA, type=float(1), shape=[?,256,256,3]) 
No variables spotted.
Found 1 possible outputs: (name=a2b_generator/output_image, op=Tanh) 
Found 11396297 (11.40M) const parameters, 0 (0) variable parameters, and 46 control_edges
Op types used: 306 Const, 154 Identity, 97 Sub, 52 Mul, 23 FusedBatchNorm, 22 Conv2D, 14 Relu, 11 Add, 10 BiasAdd, 7 StridedSlice, 4 TensorSliceDataset, 4 FilterDataset, 4 ParallelMapDataset, 4 ShuffleDataset, 4 Shape, 4 RepeatDataset, 4 BatchDataset, 4 PrefetchDataset, 3 Switch, 2 Min, 2 Conv2DBackpropInput, 2 All, 2 Assert, 2 Less, 2 Pack, 1 RandomUniform, 1 Max, 1 ReadFile, 1 RealDiv, 1 Placeholder, 1 DecodeJpeg, 1 ResizeBilinear, 1 ReverseV2, 1 GreaterEqual, 1 Equal, 1 Slice, 1 Squeeze, 1 Merge, 1 ExpandDims, 1 FloorMod, 1 Tanh, 1 RandomUniformInt
~~~~
* Optimized graph with transform_graph and freeze.py
~~~~
bazel-bin/tensorflow/tools/graph_transforms/summarize_graph --in_graph=/Users/andrewginns/Desktop/vBox/optimized_graph.pb
Found 1 possible inputs: (name=inputA, type=float(1), shape=[?,256,256,3]) 
No variables spotted.
Found 47 possible outputs: (name=a2b_generator/Conv/BatchNorm/AssignMovingAvg, op=Sub) (name=a2b_generator/Conv/BatchNorm/AssignMovingAvg_1, op=Sub) (name=a2b_generator/Conv_1/BatchNorm/AssignMovingAvg, op=Sub) (name=a2b_generator/Conv_1/BatchNorm/AssignMovingAvg_1, op=Sub) (name=a2b_generator/Conv_2/BatchNorm/AssignMovingAvg, op=Sub) (name=a2b_generator/Conv_2/BatchNorm/AssignMovingAvg_1, op=Sub) (name=a2b_generator/Conv_3/BatchNorm/AssignMovingAvg, op=Sub) (name=a2b_generator/Conv_3/BatchNorm/AssignMovingAvg_1, op=Sub) (name=a2b_generator/BatchNorm/AssignMovingAvg, op=Sub) (name=a2b_generator/BatchNorm/AssignMovingAvg_1, op=Sub) (name=a2b_generator/Conv_5/BatchNorm/AssignMovingAvg, op=Sub) (name=a2b_generator/Conv_5/BatchNorm/AssignMovingAvg_1, op=Sub) (name=a2b_generator/BatchNorm_1/AssignMovingAvg, op=Sub) (name=a2b_generator/BatchNorm_1/AssignMovingAvg_1, op=Sub) (name=a2b_generator/Conv_7/BatchNorm/AssignMovingAvg, op=Sub) (name=a2b_generator/Conv_7/BatchNorm/AssignMovingAvg_1, op=Sub) (name=a2b_generator/BatchNorm_2/AssignMovingAvg, op=Sub) (name=a2b_generator/BatchNorm_2/AssignMovingAvg_1, op=Sub) (name=a2b_generator/Conv_9/BatchNorm/AssignMovingAvg, op=Sub) (name=a2b_generator/Conv_9/BatchNorm/AssignMovingAvg_1, op=Sub) (name=a2b_generator/BatchNorm_3/AssignMovingAvg, op=Sub) (name=a2b_generator/BatchNorm_3/AssignMovingAvg_1, op=Sub) (name=a2b_generator/Conv_11/BatchNorm/AssignMovingAvg, op=Sub) (name=a2b_generator/Conv_11/BatchNorm/AssignMovingAvg_1, op=Sub) (name=a2b_generator/BatchNorm_4/AssignMovingAvg, op=Sub) (name=a2b_generator/BatchNorm_4/AssignMovingAvg_1, op=Sub) (name=a2b_generator/Conv_13/BatchNorm/AssignMovingAvg, op=Sub) (name=a2b_generator/Conv_13/BatchNorm/AssignMovingAvg_1, op=Sub) (name=a2b_generator/BatchNorm_5/AssignMovingAvg, op=Sub) (name=a2b_generator/BatchNorm_5/AssignMovingAvg_1, op=Sub) (name=a2b_generator/Conv_15/BatchNorm/AssignMovingAvg, op=Sub) (name=a2b_generator/Conv_15/BatchNorm/AssignMovingAvg_1, op=Sub) (name=a2b_generator/BatchNorm_6/AssignMovingAvg, op=Sub) (name=a2b_generator/BatchNorm_6/AssignMovingAvg_1, op=Sub) (name=a2b_generator/Conv_17/BatchNorm/AssignMovingAvg, op=Sub) (name=a2b_generator/Conv_17/BatchNorm/AssignMovingAvg_1, op=Sub) (name=a2b_generator/BatchNorm_7/AssignMovingAvg, op=Sub) (name=a2b_generator/BatchNorm_7/AssignMovingAvg_1, op=Sub) (name=a2b_generator/Conv_19/BatchNorm/AssignMovingAvg, op=Sub) (name=a2b_generator/Conv_19/BatchNorm/AssignMovingAvg_1, op=Sub) (name=a2b_generator/BatchNorm_8/AssignMovingAvg, op=Sub) (name=a2b_generator/BatchNorm_8/AssignMovingAvg_1, op=Sub) (name=a2b_generator/Conv2d_transpose/BatchNorm/AssignMovingAvg, op=Sub) (name=a2b_generator/Conv2d_transpose/BatchNorm/AssignMovingAvg_1, op=Sub) (name=a2b_generator/Conv2d_transpose_1/BatchNorm/AssignMovingAvg, op=Sub) (name=a2b_generator/Conv2d_transpose_1/BatchNorm/AssignMovingAvg_1, op=Sub) (name=a2b_generator/output_image, op=Tanh) 
Found 11396297 (11.40M) const parameters, 0 (0) variable parameters, and 0 control_edges
Op types used: 306 Const, 97 Sub, 52 Mul, 23 FusedBatchNorm, 22 Conv2D, 14 Relu, 11 Add, 10 BiasAdd, 7 StridedSlice, 5 Identity, 4 TensorSliceDataset, 4 FilterDataset, 4 ParallelMapDataset, 4 ShuffleDataset, 4 Shape, 4 RepeatDataset, 4 BatchDataset, 4 PrefetchDataset, 3 Switch, 2 Min, 2 Conv2DBackpropInput, 2 All, 2 Assert, 2 Less, 2 Pack, 1 RandomUniform, 1 Max, 1 ReadFile, 1 RealDiv, 1 Placeholder, 1 DecodeJpeg, 1 ResizeBilinear, 1 ReverseV2, 1 GreaterEqual, 1 Equal, 1 Slice, 1 Squeeze, 1 Merge, 1 ExpandDims, 1 FloorMod, 1 Tanh, 1 RandomUniformInt
~~~~
* Graph frozen with tf1.8 tools
~~~~
bazel-bin/tensorflow/tools/graph_transforms/summarize_graph --in_graph=/Users/andrewginns/Desktop/vBox/old_frozen.pb
Found 1 possible inputs: (name=inputA, type=float(1), shape=[?,256,256,3]) 
No variables spotted.
Found 1 possible outputs: (name=a2b_generator/output_image, op=Tanh) 
Found 11396297 (11.40M) const parameters, 0 (0) variable parameters, and 46 control_edges
Op types used: 306 Const, 154 Identity, 52 Mul, 51 Sub, 46 AssignSub, 23 FusedBatchNorm, 22 Conv2D, 14 Relu, 11 Add, 10 BiasAdd, 7 StridedSlice, 4 PrefetchDataset, 4 FilterDataset, 4 ParallelMapDataset, 4 TensorSliceDataset, 4 ShuffleDataset, 4 BatchDataset, 4 RepeatDataset, 4 Shape, 3 Switch, 2 Min, 2 Conv2DBackpropInput, 2 Pack, 2 All, 2 Assert, 2 Less, 1 DecodeJpeg, 1 RandomUniformInt, 1 ReadFile, 1 RealDiv, 1 Placeholder, 1 Merge, 1 ResizeBilinear, 1 ReverseV2, 1 Max, 1 GreaterEqual, 1 Slice, 1 Squeeze, 1 FloorMod, 1 ExpandDims, 1 Equal, 1 Tanh, 1 RandomUniform
~~~~
* Apart from the expanded possible output nodes in the optimised graph there are no differences
    1. No mention of any NoOp types
    2. The NoOp can only be seen in the benchmark_model
        * Not shown in tensorboard or any other tools that print nodes of the graph
    3. Becuse of the moving_mean error the graph frozen with the normal method can't be seen in tensorboard or in the other node listing tools

