#  Performance numbers

## Benchmark_model
bazel-bin/tensorflow/tools/benchmark/benchmark_model --graph=/Users/andrewginns/Desktop/vBox/optimized_graph.pb --show_sizes=false --show_flops=true --input_layer=inputA --input_layer_type=float --input_layer_shape="1,256,256,3" --output_layer=a2b_generator/output_image

### frozen_graph 94.27B
* SP4 vBox: 
* MBP 14,3: 150.97B

### optimized_graph 94.27B
* SP4 vBox: 
* MBP 14,3: 166.26B


## Python programs - On summer2winter testA first 100 images
python ckpt_a2b.py
python pb_a2b.py

### Epoch_(199)_(562of962).ckpt.data-00000-of-00001
* MBP 14,3: 74.1432 seconds, 1.349fps
* BC4 1GPU: 4.7044 seconds, 21.257fps

### frozen_graph.pb
* MBP 14,3: 69.8711 seconds, 1.431fps
* BC4 1GPU: 5.3556 seconds, 18.672fps

### optimized_graph.pb --transforms=' strip_unused_nodes(type=float, shape="1,256,256,3") remove_nodes(op=Identity, op=CheckNumerics) fold_batch_norms'
* MBP 14,3: 73.1372 seconds, 1.367fps
* BC4 1GPU: 5.2390 seconds, 19.090fps

## Python programs - On summer2winter all of testA (309 images)
python ckpt_a2b.py
python pb_a2b.py

### Epoch_(199)_(562of962).ckpt.data-00000-of-00001
* MBP 14,3:  234.1944 seconds, fps
* BC4 1GPU:  12.6921 seconds, fps

### frozen_graph.pb
* MBP 14,3:  218.7996 seconds, fps
* BC4 1GPU:  13.2439 seconds, 23.331fps

### optimized_graph.pb --transforms=' strip_unused_nodes(type=float, shape="1,256,256,3") remove_nodes(op=Identity, op=CheckNumerics) fold_batch_norms'
* MBP 14,3:  228.1911 seconds, fps
* BC4 1GPU:  12.8100 seconds, 24.122fps

