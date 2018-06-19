# Performance numbers
### frozen_graph.pb
  * GrafDef generated from frozen .ckpt files
  * 94.27B
  * 45.9MB
  * 501 nodes

### optimized_graph.pb
  * 94.27B
  * 45.9MB
  * 243 nodes
~~~~
--transforms=' strip_unused_nodes(type=float, shape="1,256,256,3") remove_nodes(op=Identity, op=CheckNumerics) fold_batch_norms sort_by_execution_order'
~~~~

#### quant_optimized_graph
  * 94.27B
  * 11.7MB
  * 500 nodes
~~~~
--transforms=' strip_unused_nodes(type=float, shape="1,256,256,3") remove_nodes(op=Identity, op=CheckNumerics) fold_batch_norms quantize_weights quantize_nodes strip_unused_nodes sort_by_execution_order '
~~~~

#### Epoch_(199)_(562of962).ckpt.data-00000-of-00001
* 339.7MB
* CycleGAN trained on summer2winter_yosemite dataset with 200 Epochs and default crop size    

# Observations
* Running quantized graphs on GPUs results in extremely low amounts of GPU usage and low performance
    * Due to lack of support for quantized inference on GPUs in TF at the moment (tfr1.8)

# Bazel benchmark
~~~~
bazel-bin/tensorflow/tools/benchmark/benchmark_model --graph=/Users/andrewginns/Desktop/vBox/CycleGAN-Tensorflow-PyTorch/outputs/checkpoints/summer2winter_yosemite/optimized_graph.pb --show_sizes=false --show_flops=true --input_layer=inputA --input_layer_type=float --input_layer_shape="1,256,256,3" --output_layer=a2b_generator/output_image
~~~~

## CycleGAN-Tensorflow-Pytorch
### frozen_graph
* SP4 vBox: 
* MBP 14,3: 138.93B
* AMD x4 835: 36.28B
* Pixel 2XL armv8a: 23.96B
* Pixel 2XL armv7a: 20.09B

### optimized_graph
* SP4 vBox: 
* MBP 14,3: 140.74B
* AMD x4 835: 36.25B
* Pixel 2XL armv8a: 23.88B
* Pixel 2XL armv7a: 19.43B

### quant_optimized_graph
* SP4 vBox: 
* MBP 14,3: 
* AMD x4 835: 3.43B
* Pixel 2XL armv8a: 20.38B
* Pixel 2XL armv7a: 18.55B

## CycleGAN-Tensorflow-Simple
### frozen_graph
* SP4 vBox: 
* MBP 14,3: 125.97B

### optimized_graph
* SP4 vBox: 
* MBP 14,3: 123.86B

# Python benchmark
~~~~
python ckpt_a2b.py --checkpoints='/path/to/checkpoints.ckpt' --dataset='/path/to/images_folder'

python pb_a2b.py --graph='/path/to/.pb' --dataset='/path/to/image_folder'
~~~~

## summer2winter testA first 100 images, CycleGAN-Tensorflow-Pytorch

### Epoch_(199)_(562of962).ckpt.data-00000-of-00001
* MBP 14,3: 74.1432 seconds, 1.349fps
* BC4 1GPU: 4.7044 seconds, 21.257fps
* AMD x4 835:  seconds, fps

### frozen_graph
* MBP 14,3: 69.8711 seconds, 1.431fps
* BC4 1GPU: 5.3556 seconds, 18.672fps
* AMD x4 835: 271.3400 seconds, 0.369fps

### optimized_graph
* MBP 14,3: 73.1372 seconds, 1.367fps
* BC4 1GPU: 5.2390 seconds, 19.090fps
* AMD x4 835: 

### quant_optimized_graph
* MBP 14,3: 
* BC4 1GPU: 655.5881 seconds, 0.153fps
* AMD x4 835: 2892.9575 seconds, 0.035fps

## summer2winter all of testA (309 images)

### Epoch_(199)_(562of962).ckpt.data-00000-of-00001
* MBP 14,3:  234.1944 seconds, 1.319fps
* BC4 1GPU:  12.6921 seconds, 24.346fps
* AMD x4 835:  seconds, fps

### frozen_graph
* MBP 14,3:  218.7996 seconds, 1.412fps
* BC4 1GPU:  13.2439 seconds, 23.331fps
* AMD x4 835: 828.2682 seconds, 0.373fps

### optimized_graph
* MBP 14,3:  228.1911 seconds, 1.354fps
* BC4 1GPU:  12.8100 seconds, 24.122fps
* AMD x4 835: 

### quant_optimized_graph
* MBP 14,3: 
* BC4 1GPU: 1999.4155 seconds, 0.155fps
* AMD x4 835: 8845.4588 seconds, 0.035fps
