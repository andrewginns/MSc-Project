# Step-by-Step Instructions for project flow
* Install tensorflow 1.6, bazel 0.11.0 and MNC SDK 2.04

* Train network
  1. CUDA_VISIBLE_DEVICES=0 python train.py --dataset=summer2winter_yosemite
  
* Freeze the output files
  1. Use freeze.py
  
* Optimize the graph
  1. bazel-bin/tensorflow/tools/graph_transforms/transform_graph --in_graph=/Users/andrewginns/Desktop/vBox/frozen_graph.pb --out_graph=/Users/andrewginns/Desktop/vBox/optimized_graph.pb --inputs=‘inputA’ --outputs='a2b_generator/output_image' --transforms=' strip_unused_nodes(type=float, shape="1,256,256,3") remove_nodes(op=Identity, op=CheckNumerics) fold_batch_norms'
    
* Benchmark to make sure all ops are listed and graph runs
  1. bazel-bin/tensorflow/tools/benchmark/benchmark_model --graph=/Users/andrewginns/Desktop/vBox/optimized_graph.pb --show_sizes=false --show_flops=true --input_layer=inputA --input_layer_type=float --input_layer_shape="1,256,256,3" --output_layer=a2b_generator/output_image

* Convert to a movidius graph
  1. mvNCCompile /media/sf_vBox/optimized_graph.pb -in inputA -on a2b_generator/output_image
