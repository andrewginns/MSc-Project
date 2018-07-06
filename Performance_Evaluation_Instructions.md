# Performance Evaluation Instructions

Lists all the ops in the model and evaluate performance on different hardware

## Requirements

- Tested on macOS 10.13 and Ubuntu 16.04.4
- Python 2.7.12
- pip 8.1+
- six
- numpy
- Tensorflow 1.8+ source files
- Bazel 0.10.0 or 0.11.0 https://github.com/bazelbuild/bazel/releases
- Android Studio: Android SDK level 27, Build tools 27.0.3, NDK version 15

## Desktop benchmarking

### GraphDef (.pb)

```
bazel-bin/tensorflow/tools/benchmark/benchmark_model --graph=/Users/andrewginns/Desktop/vBox/CycleGAN-Tensorflow-PyTorch/outputs/checkpoints/summer2winter_yosemite/optimized_graph.pb --show_sizes=false --show_flops=true --input_layer=inputA --input_layer_type=float --input_layer_shape="1,256,256,3" --output_layer=a2b_generator/output_image
```

### TFLite (.tflite)

```
bazel-bin/tensorflow/contrib/lite/tools/benchmark/benchmark_model --graph=graph.lite --input_layer="inputA" --input_layer_shape="1,256,256,3" --num_threads=4
```

## Mobile benchmarking

### GraphDef (.pb)

```
adb push bazel-bin/tensorflow/tools/benchmark/benchmark_model /data/local/tmp

adb push /Users/andrewginns/Desktop/vBox/CycleGAN-Tensorflow-PyTorch/outputs/checkpoints/summer2winter_yosemite/quant_optimized_graph.pb /data/local/tmp/

adb shell "/data/local/tmp/benchmark_model --graph=/data/local/tmp/quant_optimized_graph.pb --show_sizes=false --show_flops=true --input_layer=inputA --input_layer_type=float --input_layer_shape="1,256,256,3" --output_layer=a2b_generator/output_image"
```

### TFLite (.tflite)

```
adb push bazel-bin/tensorflow/contrib/lite/tools/benchmark/benchmark_model /data/local/tmp

adb shell chmod +x /data/local/tmp/benchmark_model

adb push graph.tflite /data/local/tmp

adb shell tasket f0 /data/local/tmp/benchmark_model --graph=/data/local/tmp/graph-float.tflite --input_layer="inputA" --input_layer_shape="1,256,256,3" --num_threads=4
```

## 
