#  Current problems
## The problem as well as steps to reproduce and fixes in progress (if any)

### 1. TFLite Android cannot create a MappedByteBuffer of the tflite model
* Tested in both the tensorflow-for-poets-2 codelab and a basic TFLite wrapper
* Model can be successfully mapped and benchmarked using tensorflow/contrib/lite/tools/benchmark:benchmark_model

```
A/libc: Fatal signal 6 (SIGABRT), code -6 in tid 4333 (dp.thexor), pid 4333 (dp.thexor)
```

Seems to be linked to an incorrect startOffset and declaredLength values
* Fixing these values to a known-good constant from another model allows the model to load successfully.

StackOverflow issue posted here https://stackoverflow.com/questions/51341554/tflite-android-mode-file-will-not-load-startoffset-and-declaredlength-problems

### 2. TFLite becnhmark can't use the NNAPI
The NNAPI works when enabled on a demonstration tflite model. When enabled on my own model through
```
 adb shell taskset f0 /data/local/tmp/benchmark_model --graph=/data/local/tmp/graph-float.tflite --input_layer="inputA" --input_layer_shape="1,256,256,3" --num_threads=-1 --num_runs=20 --use_nnapi=true
```
The output is
```
STARTING!
Num runs: [20]
Inter-run delay (seconds): [-1]
Num threads: [-1]
Benchmark name: []
Output prefix: []
Warmup runs: [1]
Graph: [/data/local/tmp/graph-float.tflite]
Input layers: [inputA]
Input shapes: [1,256,256,3]
Use nnapi : [1]
Loaded model /data/local/tmp/graph-float.tflite
resolved reporter
Initialized session in 76.197ms
Running benchmark for 1 iterations 
Op code 67 is currently not delegated to NNAPI
Returning error since NNAPI returned failure nnapi_delegate.cc:664.
Failed to build graph for NNAPI
Failed to invoke!
Aborted
```
I imagine this is either due to my model being a floating point one instead of a uint8 model.

### 3. TFLite does not support required quantised ops in the model
The TransposeConv op does not have a quantised op equivalent. This means that the generated .tflite model uses float operations instead of uint8 operations.

TransposeConv is a convolution going in the opposite direction to a standard convolution. This goes from the shape of the output to the shape of the input.

```
tflite_convert --output_file=graph-fakequant.tflite --graph_def_file=frozen_graph.pb --inference_type=QUANTIZED_UINT8 --input_arrays=inputA --output_arrays=a2b_generator/output_image --default_ranges_min=0 --default_ranges_max=6 --mean_values=128 --std_dev_values=127
```

This affects both the toco and tflite_convert commands.
```
2018-07-06 11:12:23.485598: F tensorflow/contrib/lite/toco/graph_transformations/quantize.cc:457] Unimplemented: this graph contains an operator of type TransposeConv for which the quantized form is not yet implemented. Sorry, and patches welcome (that's a relatively fun patch to write, mostly providing the actual quantized arithmetic code for this op).
Aborted (core dumped)
```
* May be possible to create the required patch
* Otherwise wait for implementation
    
### 4. Movidius mvNCCompile gives a compilation error when attempting to convert the graph
```
mvNCCompile /tmp/mov.pb -in inputA -on a2b_generator/output_image
/usr/local/bin/ncsdk/Controllers/Parsers/TensorFlowParser/Convolution.py:44: SyntaxWarning: assertion is always true, perhaps remove parentheses?
  assert(False, "Layer type not supported by Convolution: " + obj.type)
mvNCCompile v02.00, Copyright @ Intel Corporation 2017

/usr/local/lib/python3.5/dist-packages/tensorflow/python/util/tf_inspect.py:45: DeprecationWarning: inspect.getargspec() is deprecated, use inspect.signature() instead
Traceback (most recent call last):
  File "/usr/local/lib/python3.5/dist-packages/tensorflow/python/framework/common_shapes.py", line 686, in _call_cpp_shape_fn_impl
    input_tensors_as_shapes, status)
  File "/usr/local/lib/python3.5/dist-packages/tensorflow/python/framework/errors_impl.py", line 516, in __exit__
    c_api.TF_GetCode(self.status.status))
tensorflow.python.framework.errors_impl.InvalidArgumentError: Shape must be rank 4 but is rank 0 for 'a2b_generator/Conv2d_transpose/conv2d_transpose' (op: 'Conv2DBackpropInput') with input shapes: ?, ?, ? and with input tensors computed as partial shapes: input[0] = [].

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/local/bin/mvNCCompile", line 169, in <module>
    create_graph(args.network, args.image, args.inputnode, args.outputnode, args.outfile, args.nshaves, args.inputsize, args.weights, args.explicit_concat, args.ma2480, args.scheduler, args.new_parser, args)
  File "/usr/local/bin/mvNCCompile", line 148, in create_graph
    load_ret = load_network(args, parser, myriad_config)
  File "/usr/local/bin/ncsdk/Controllers/Scheduler.py", line 100, in load_network
    parse_ret = parse_tensor(arguments, myriad_conf)
  File "/usr/local/bin/ncsdk/Controllers/TensorFlowParser.py", line 212, in parse_tensor
    tf.import_graph_def(graph_def, name="")
  File "/usr/local/lib/python3.5/dist-packages/tensorflow/python/util/deprecation.py", line 432, in new_func
    return func(*args, **kwargs)
  File "/usr/local/lib/python3.5/dist-packages/tensorflow/python/framework/importer.py", line 687, in import_graph_def
    ops.set_shapes_for_outputs(op)
  File "/usr/local/lib/python3.5/dist-packages/tensorflow/python/framework/ops.py", line 2496, in set_shapes_for_outputs
    return _set_shapes_for_outputs(op)
  File "/usr/local/lib/python3.5/dist-packages/tensorflow/python/framework/ops.py", line 2469, in _set_shapes_for_outputs
    shapes = shape_func(op)
  File "/usr/local/lib/python3.5/dist-packages/tensorflow/python/framework/ops.py", line 2399, in call_with_requiring
    return call_cpp_shape_fn(op, require_shape_fn=True)
  File "/usr/local/lib/python3.5/dist-packages/tensorflow/python/framework/common_shapes.py", line 627, in call_cpp_shape_fn
    require_shape_fn)
  File "/usr/local/lib/python3.5/dist-packages/tensorflow/python/framework/common_shapes.py", line 691, in _call_cpp_shape_fn_impl
    raise ValueError(err.message)
ValueError: Shape must be rank 4 but is rank 0 for 'a2b_generator/Conv2d_transpose/conv2d_transpose' (op: 'Conv2DBackpropInput') with input shapes: ?, ?, ? and with input tensors computed as partial shapes: input[0] = [].
```
  * A dialogue has been opened with Movidius support about this https://ncsforum.movidius.com/discussion/865/conversion-of-

### 5. Quantized nodes give incorrect output in the model
The GrafDef generated with a quantized_nodes transform applied produces incorrect output. The Quantised model (quant_quant.pb)

```
bazel build --config=opt tensorflow/tools/graph_transforms:transform_graph && bazel-bin/tensorflow/tools/graph_transforms/transform_graph --in_graph=/tmp/frozen-graph.pb --out_graph=/tmp/optimized-graph.pb --inputs=‘inputA’ --outputs='a2b_generator/output_image' --transforms='add_default_attributes fold_constants(ignore_errors=true) fold_batch_norms quantize_weights quantize_nodes sort_by_execution_order'
```
Possibly due to the incorrect quantization of the colour values in the network meaning that the colours are not preserved correctly.

    
# Solved

### Solved by adding add_shape=True to freeze graph program
1. Movidius mvNCCompile gives a compilation error when attempting to convert the graph
```
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
```
  * A dialogue has been opened with Movidius support about this https://ncsforum.movidius.com/discussion/865/conversion-of-frozen-tensorflow-graph-to-movidius-graph#latest
  
  * Issue has been narrowed down to the Placeholder Tensor. This has the shape ?, 600,600,3 which the conversion tool seems to not like.

### Solved by writing own freeze graph script
1. The default freeze_graph does not work on CycleGAN due to moving_mean ops
* A custom implementation of freeze.py is implemented instead

### Solved using the TF1.8 tools
1. freeze.py seems to introduce a node called _SOURCE with type 'NoOp' 
    * This is causing problems with the TFLite conversion
```
toco --input_file=/Users/andrewginns/Desktop/vBox/optimized_graph.pb \
    >   --output_file=/Users/andrewginns/Desktop/vBox/graph.lite \
    >   --input_format=TENSORFLOW_GRAPHDEF \
    >   --output_format=TFLITE \
    >   --input_shape=1,256,256,3 \
    >   --input_array=inputA \
    >   --output_array=a2b_generator/output_image
    2018-06-16 14:47:07.775019: F tensorflow/core/graph/graph.cc:283] Non-OK-status: status status: Not found: Op type not registered 'NoOp' in binary running on Andrews-MacBook-Pro.local. Make sure the Op and Kernel are registered in the binary running in this process.
    Abort trap: 6
```
    
2. Investigating problem 2 using summarize_graph seems to give the same output
* Graph frozen with freeze.py
```
bazel-bin/tensorflow/tools/graph_transforms/summarize_graph --in_graph=/Users/andrewginns/Desktop/vBox/frozen_graph.pb
Found 1 possible inputs: (name=inputA, type=float(1), shape=[?,256,256,3]) 
No variables spotted.
Found 1 possible outputs: (name=a2b_generator/output_image, op=Tanh) 
Found 11396297 (11.40M) const parameters, 0 (0) variable parameters, and 46 control_edges
Op types used: 306 Const, 154 Identity, 97 Sub, 52 Mul, 23 FusedBatchNorm, 22 Conv2D, 14 Relu, 11 Add, 10 BiasAdd, 7 StridedSlice, 4 TensorSliceDataset, 4 FilterDataset, 4 ParallelMapDataset, 4 ShuffleDataset, 4 Shape, 4 RepeatDataset, 4 BatchDataset, 4 PrefetchDataset, 3 Switch, 2 Min, 2 Conv2DBackpropInput, 2 All, 2 Assert, 2 Less, 2 Pack, 1 RandomUniform, 1 Max, 1 ReadFile, 1 RealDiv, 1 Placeholder, 1 DecodeJpeg, 1 ResizeBilinear, 1 ReverseV2, 1 GreaterEqual, 1 Equal, 1 Slice, 1 Squeeze, 1 Merge, 1 ExpandDims, 1 FloorMod, 1 Tanh, 1 RandomUniformInt
```
* Optimized graph with transform_graph and freeze.py
```
bazel-bin/tensorflow/tools/graph_transforms/summarize_graph --in_graph=/Users/andrewginns/Desktop/vBox/optimized_graph.pb
Found 1 possible inputs: (name=inputA, type=float(1), shape=[?,256,256,3]) 
No variables spotted.
Found 47 possible outputs: (name=a2b_generator/Conv/BatchNorm/AssignMovingAvg, op=Sub) (name=a2b_generator/Conv/BatchNorm/AssignMovingAvg_1, op=Sub) (name=a2b_generator/Conv_1/BatchNorm/AssignMovingAvg, op=Sub) (name=a2b_generator/Conv_1/BatchNorm/AssignMovingAvg_1, op=Sub) (name=a2b_generator/Conv_2/BatchNorm/AssignMovingAvg, op=Sub) (name=a2b_generator/Conv_2/BatchNorm/AssignMovingAvg_1, op=Sub) (name=a2b_generator/Conv_3/BatchNorm/AssignMovingAvg, op=Sub) (name=a2b_generator/Conv_3/BatchNorm/AssignMovingAvg_1, op=Sub) (name=a2b_generator/BatchNorm/AssignMovingAvg, op=Sub) (name=a2b_generator/BatchNorm/AssignMovingAvg_1, op=Sub) (name=a2b_generator/Conv_5/BatchNorm/AssignMovingAvg, op=Sub) (name=a2b_generator/Conv_5/BatchNorm/AssignMovingAvg_1, op=Sub) (name=a2b_generator/BatchNorm_1/AssignMovingAvg, op=Sub) (name=a2b_generator/BatchNorm_1/AssignMovingAvg_1, op=Sub) (name=a2b_generator/Conv_7/BatchNorm/AssignMovingAvg, op=Sub) (name=a2b_generator/Conv_7/BatchNorm/AssignMovingAvg_1, op=Sub) (name=a2b_generator/BatchNorm_2/AssignMovingAvg, op=Sub) (name=a2b_generator/BatchNorm_2/AssignMovingAvg_1, op=Sub) (name=a2b_generator/Conv_9/BatchNorm/AssignMovingAvg, op=Sub) (name=a2b_generator/Conv_9/BatchNorm/AssignMovingAvg_1, op=Sub) (name=a2b_generator/BatchNorm_3/AssignMovingAvg, op=Sub) (name=a2b_generator/BatchNorm_3/AssignMovingAvg_1, op=Sub) (name=a2b_generator/Conv_11/BatchNorm/AssignMovingAvg, op=Sub) (name=a2b_generator/Conv_11/BatchNorm/AssignMovingAvg_1, op=Sub) (name=a2b_generator/BatchNorm_4/AssignMovingAvg, op=Sub) (name=a2b_generator/BatchNorm_4/AssignMovingAvg_1, op=Sub) (name=a2b_generator/Conv_13/BatchNorm/AssignMovingAvg, op=Sub) (name=a2b_generator/Conv_13/BatchNorm/AssignMovingAvg_1, op=Sub) (name=a2b_generator/BatchNorm_5/AssignMovingAvg, op=Sub) (name=a2b_generator/BatchNorm_5/AssignMovingAvg_1, op=Sub) (name=a2b_generator/Conv_15/BatchNorm/AssignMovingAvg, op=Sub) (name=a2b_generator/Conv_15/BatchNorm/AssignMovingAvg_1, op=Sub) (name=a2b_generator/BatchNorm_6/AssignMovingAvg, op=Sub) (name=a2b_generator/BatchNorm_6/AssignMovingAvg_1, op=Sub) (name=a2b_generator/Conv_17/BatchNorm/AssignMovingAvg, op=Sub) (name=a2b_generator/Conv_17/BatchNorm/AssignMovingAvg_1, op=Sub) (name=a2b_generator/BatchNorm_7/AssignMovingAvg, op=Sub) (name=a2b_generator/BatchNorm_7/AssignMovingAvg_1, op=Sub) (name=a2b_generator/Conv_19/BatchNorm/AssignMovingAvg, op=Sub) (name=a2b_generator/Conv_19/BatchNorm/AssignMovingAvg_1, op=Sub) (name=a2b_generator/BatchNorm_8/AssignMovingAvg, op=Sub) (name=a2b_generator/BatchNorm_8/AssignMovingAvg_1, op=Sub) (name=a2b_generator/Conv2d_transpose/BatchNorm/AssignMovingAvg, op=Sub) (name=a2b_generator/Conv2d_transpose/BatchNorm/AssignMovingAvg_1, op=Sub) (name=a2b_generator/Conv2d_transpose_1/BatchNorm/AssignMovingAvg, op=Sub) (name=a2b_generator/Conv2d_transpose_1/BatchNorm/AssignMovingAvg_1, op=Sub) (name=a2b_generator/output_image, op=Tanh) 
Found 11396297 (11.40M) const parameters, 0 (0) variable parameters, and 0 control_edges
Op types used: 306 Const, 97 Sub, 52 Mul, 23 FusedBatchNorm, 22 Conv2D, 14 Relu, 11 Add, 10 BiasAdd, 7 StridedSlice, 5 Identity, 4 TensorSliceDataset, 4 FilterDataset, 4 ParallelMapDataset, 4 ShuffleDataset, 4 Shape, 4 RepeatDataset, 4 BatchDataset, 4 PrefetchDataset, 3 Switch, 2 Min, 2 Conv2DBackpropInput, 2 All, 2 Assert, 2 Less, 2 Pack, 1 RandomUniform, 1 Max, 1 ReadFile, 1 RealDiv, 1 Placeholder, 1 DecodeJpeg, 1 ResizeBilinear, 1 ReverseV2, 1 GreaterEqual, 1 Equal, 1 Slice, 1 Squeeze, 1 Merge, 1 ExpandDims, 1 FloorMod, 1 Tanh, 1 RandomUniformInt
```
* Graph frozen with tf1.8 tools
```
bazel-bin/tensorflow/tools/graph_transforms/summarize_graph --in_graph=/Users/andrewginns/Desktop/vBox/old_frozen.pb
Found 1 possible inputs: (name=inputA, type=float(1), shape=[?,256,256,3]) 
No variables spotted.
Found 1 possible outputs: (name=a2b_generator/output_image, op=Tanh) 
Found 11396297 (11.40M) const parameters, 0 (0) variable parameters, and 46 control_edges
Op types used: 306 Const, 154 Identity, 52 Mul, 51 Sub, 46 AssignSub, 23 FusedBatchNorm, 22 Conv2D, 14 Relu, 11 Add, 10 BiasAdd, 7 StridedSlice, 4 PrefetchDataset, 4 FilterDataset, 4 ParallelMapDataset, 4 TensorSliceDataset, 4 ShuffleDataset, 4 BatchDataset, 4 RepeatDataset, 4 Shape, 3 Switch, 2 Min, 2 Conv2DBackpropInput, 2 Pack, 2 All, 2 Assert, 2 Less, 1 DecodeJpeg, 1 RandomUniformInt, 1 ReadFile, 1 RealDiv, 1 Placeholder, 1 Merge, 1 ResizeBilinear, 1 ReverseV2, 1 Max, 1 GreaterEqual, 1 Slice, 1 Squeeze, 1 FloorMod, 1 ExpandDims, 1 Equal, 1 Tanh, 1 RandomUniform
```
* Apart from the expanded possible output nodes in the optimised graph there are no differences
    1. No mention of any NoOp types
    2. The NoOp can only be seen in the benchmark_model
        * Not shown in tensorboard or any other tools that print nodes of the graph
    3. Becuse of the moving_mean error the graph frozen with the normal method can't be seen in tensorboard or in the other node listing tools
    
### Solved using bazel 0.10.1 and installing NDK 15
1. The bazel benchmark_model for android is not compiling properly for arm64-v8a
```
bazel build -c opt --cxxopt='--std=c++11' //tensorflow/tools/benchmark:benchmark_model --crosstool_top=//external:android/crosstool --host_crosstool_top=@bazel_tools//tools/cpp:toolchain --cpu=arm64-v8a --verbose_failures
ERROR: No default_toolchain found for cpu 'arm64-v8a'. Valid cpus are: [
k8,
local,
armeabi-v7a,
x64_windows,
x64_windows_msvc,
x64_windows_msys,
s390x,
ios_x86_64,
]
INFO: Elapsed time: 0.315s
INFO: 0 processes.
FAILED: Build did NOT complete successfully (0 packages loaded)
```
* https://stackoverflow.com/questions/50915090/how-to-build-tensorflow-benchmark-model-for-android-arm64-v8a
https://developer.android.com/ndk/guides/


### Solved by converting colour space values
1. The Android app is not showing a live preview of the network output properly
    * Probably due to incorrect conversion of the RGB output from the network to a Bitmapped image

### Solved by cloning, making and linking flatbuffers manually
1. Visualisation tools for TFLite graphs are broken
```
bazel-bin/tensorflow/contrib/lite/tools/visualize foo.tflite foo.html
```
Leads to an error about flatbuffers/flatc not found.
https://github.com/tensorflow/tensorflow/issues/18857

1. Clone https://github.com/google/flatbuffers
2. Extract and navigate to the flatbuffers-master folder
3. Run the appropriate cmake command
```
cmake -G "Unix Makefiles"
cmake -G "Visual Studio 10"
cmake -G "Xcode"
```
4. Make
```
make
```
5. Test that it was successful
```
./flattests
```
6. Navigate to your tensorflow-master folder
7. Edit tensorflow/contrib/lite/tools/visualize.py
- Change the _BINARY = path/to/flatc/file/in/cloned/flatbuffers/folder
- Change the _SCHEMA =absolute/path/to/schema.fbs
8. Your TFLite visualise command should now work!

For reference my paths looks like:
```
_SCHEMA = "home/user/Downloads/tensorflow-master/tensorflow/contrib/lite/schema/schema.fbs"
_BINARY = "home/user/Downloads/flatbuffers-master/flatc"
```
