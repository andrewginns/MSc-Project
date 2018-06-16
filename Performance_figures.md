#  Performance numbers

bazel-bin/tensorflow/tools/benchmark/benchmark_model --graph=/Users/andrewginns/Desktop/vBox/optimized_graph.pb --show_sizes=false --show_flops=true --input_layer=inputA --input_layer_type=float --input_layer_shape="1,256,256,3" --output_layer=a2b_generator/output_image

## optimized_graph 94.27B
* SP4 vBox: 
* MBP 14,3: 166.26B

