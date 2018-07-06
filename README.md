# MSc-Project
Work carried out for the completion an MSc degree in Advanced Computing at the University of Bristol

## Full Requirements

- Tested on macOS 10.13 and Ubuntu 16.04.4

- Python 2.7.12

- pip 8.1+

- six

- numpy

- Tensorflow 1.6 source files

- Tensorflow 1.8+ source files

- Bazel 0.10.0 or 0.11.0 https://github.com/bazelbuild/bazel/releases

- Android Studio: Android SDK level 27, Build tools 27.0.3, NDK version 15

- CycleGAN Android app

  - CycleGAN Capture - Single image Style-Transfer <https://github.com/andrewginns/CycleGAN-Capture>
  - CycleGAN View - Live preview Style-Transfer <https://github.com/andrewginns/CycleGAN-TF-Android>
- Movidius Neural Compute Stick (MNCS) 

  - Movidius Neural Compute SDK 2.04+ https://github.com/movidius/ncsdk/releases

## Source Code

https://github.com/andrewginns/CycleGAN-Tensorflow-PyTorch

Pre-built models:

https://github.com/andrewginns/CycleGAN-Tensorflow-PyTorch/releases

It is recommended that the these instructions are followed before the main documentation:

#### Tensorflow from source

https://github.com/andrewginns/MSc-Project/blob/master/Tensorflow_Build_Instructions.md

#### Tensorflow tools

https://github.com/andrewginns/MSc-Project/blob/master/Tensorflow_Tools_Build_Instructions.md



## Documentation

#### Training

https://github.com/andrewginns/MSc-Project/blob/master/Training_Instructions.md

#### Inference

https://github.com/andrewginns/MSc-Project/blob/master/Inference_Instructions.md

#### Optimisation

https://github.com/andrewginns/MSc-Project/blob/master/Model_Optimisation_Instructions.md

#### Benchmarking

https://github.com/andrewginns/MSc-Project/blob/master/Performance_Evaluation_Instructions.md

#### Current problems

https://github.com/andrewginns/MSc-Project/blob/master/Current_Problems.md



## Android Apps

  * CycleGAN Capture - Single image Style-Transfer https://github.com/andrewginns/CycleGAN-Capture
  * CycleGAN View - Live preview Style-Transfer https://github.com/andrewginns/CycleGAN-TF-Android



## Other tools

#### Summarize GrafDef proto to view nodes and other info

```
bazel-bin/tensorflow/tools/graph_transforms/summarize_graph --in_graph=path/to/graph.pb
```

#### View the graph in Tensorboard

```
tensorboard --logdir=logs/ --host localhost --port 8088
```

#### Summarize the GraphDef to view nodes and other info, should be reduced compared to the graph.pb

```
bazel-bin/tensorflow/tools/graph_transforms/summarize_graph --in_graph=/tmp/frozen_graph.pb
```



## Useful commands

#### Bazel

  Remove bazel - Linux

```
rm -rf ~/.bazel ~/.bazelrc ~/.cache/bazel
```

  Remove bazel - macOS

```
rm -rf /usr/local/bin/bazel /usr/local/bin/bazel /usr/local/lib/bazel
```

  Install bazel

```
sudo apt-get install pkg-config zip g++ zlib1g-dev unzip python

wget https://github.com/bazelbuild/bazel/releases/download/0.11.0/bazel-0.11.0-installer-linux-x86_64.sh

chmod +x bazel-0.11.0-installer-linux-x86_64.sh

./bazel-0.11.0-installer-linux-x86_64.sh --user

export PATH="$PATH:$HOME/bin"
```



## Additional Resources

Tensorflow reference

* https://www.tensorflow.org/api_docs/

Graph Transform Tools reference

- https://github.com/tensorflow/tensorflow/blob/r1.6/tensorflow/tools/graph_transforms/README.md
- https://www.tensorflow.org/versions/r1.6/mobile/prepare_models

Movidius Reference

- https://movidius.github.io/ncsdk/

  TFLite reference

- https://github.com/tensorflow/tensorflow/blob/master/tensorflow/contrib/lite/toco/g3doc/cmdline_examples.md