# Performance Evaluation Instructions

Lists all the ops in the model and evaluate performance on different hardware
https://docs.google.com/spreadsheets/d/1_2VHXeiNVBB-4_zcDo2q9ygWWfR14UTl3hZa7M8g1vo/edit?usp=sharing

## Requirements

- Tested on macOS 10.13 and Ubuntu 16.04.4
- Python 2.7.12
- pip 8.1+
- six
- numpy
- Tensorflow 1.8+ source files with a configured WORKSPACE
- Bazel 0.10.0 or 0.11.0 https://github.com/bazelbuild/bazel/releases
- Android Studio: Android SDK level 27, Build tools 27.0.3, NDK version 15

## Desktop benchmarking

### GraphDef (.pb)
bazel 0.15.0, SDK API level 27, NDK 15, Build tools 27.0.3, tensorflow 1.10
Bazel benchmark
```
bazel build --config=opt tensorflow/tools/benchmark:benchmark_model && bazel-bin/tensorflow/tools/benchmark/benchmark_model --graph=/Users/andrewginns/Desktop/vBox/CycleGAN-Tensorflow-PyTorch/outputs/checkpoints/summer2winter_yosemite/optimized_graph.pb --show_sizes=false --show_flops=true --input_layer=inputA --input_layer_type=float --input_layer_shape="1,256,256,3" --output_layer=a2b_generator/output_image --num_threads=-1
```

Python benchmark
```
python pb_a2b.py --graph='/path/to/.pb' --dataset='/path/to/image_folder'
```

### TFLite (.tflite)
bazel 0.15.0, SDK API level 27, NDK 15, Build tools 27.0.3, tensorflow 1.10
```
bazel build --config=opt tensorflow/contrib/lite/tools/benchmark:benchmark_model && bazel-bin/tensorflow/contrib/lite/tools/benchmark/benchmark_model --graph=graph-float.tflite --input_layer="inputA" --input_layer_shape="1,256,256,3" --num_threads=-1
```

### Checkpoints (.ckpt)

Python benchmark
```
python ckpt_a2b.py --checkpoints='/path/to/checkpoints.ckpt' --dataset='/path/to/images_folder'
```

## Mobile benchmarking

### GraphDef (.pb)
bazel 0.10.1, SDK API level 27, NDK 15, Build tools 27.0.3, tensorflow 1.8

```
bazel build --config=monolithic --cxxopt=--std=c++11 //tensorflow/tools/benchmark:benchmark_model --config=android_arm64 --cpu=arm64-v8a

adb push bazel-bin/tensorflow/tools/benchmark/benchmark_model /data/local/tmp

adb push /Users/andrewginns/Desktop/vBox/CycleGAN-Tensorflow-PyTorch/outputs/checkpoints/summer2winter_yosemite/quant_optimized_graph.pb /data/local/tmp/

adb shell taskset f0 "/data/local/tmp/benchmark_model --graph=/data/local/tmp/optimized_graph.pb --show_sizes=false --show_flops=true --input_layer=inputA --input_layer_type=float --input_layer_shape="1,256,256,3" --output_layer=a2b_generator/output_image" --num_threads=-1
```

### TFLite (.tflite)
bazel 0.15.0, SDK API level 27, NDK 15, Build tools 27.0.3, tensorflow 1.10
```

bazel build -c opt \
  --config=android_arm \
  --cxxopt='--std=c++11' \
  tensorflow/contrib/lite/tools/benchmark:benchmark_model

adb push bazel-bin/tensorflow/contrib/lite/tools/benchmark/benchmark_model /data/local/tmp/tflite/benchmark_model

adb shell chmod +x /data/local/tmp/tflite/benchmark_model

adb push float.tflite /data/local/tmp

adb shell taskset f0 /data/local/tmp/tflite/benchmark_model --graph=/data/local/tmp/float.tflite --input_layer="inputA" --input_layer_shape="1,256,256,3" --num_threads=-1

```

## Errors
If you are having errors that look similar to:
```
C++ compilation of rule '//tensorflow/contrib/lite/tools/benchmark:benchmark_model_lib' failed (Exit 1)
```
Then a liklely cause is that WORKSPACE isn't properly configured through the ./configure command. Check the SDK and NDK paths.
