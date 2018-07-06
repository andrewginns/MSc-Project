# Tensorflow Build Instructions

## Requirements

- Tested on macOS 10.13 and Ubuntu 16.04.4
- Python 2.7.12
- pip 8.1+
- six
- numpy
- Bazel 0.10.0 or 0.11.0 https://github.com/bazelbuild/bazel/releases

## Tensorflow CPU Build

Tensorflow only needs to be built from source if you want to customise the use of AVX, AVX2 and FMA instructions. These can result in significant speedup. Tested on Ubuntu 16.04.4 and macOS 10.13

- Requires a working bazel install (Tested on bazel 0.10.0 and 0.11.0)
- Building from source can enable significant speedup compared to using an official pre-built .whl
- The official pre-built .whl files for Tensorflow 1.6+ have AVX enabled by default. Older CPUs may need .whl packages built from source without AVX
- My custom pre-built files https://github.com/andrewginns/tflow-whls
  - Includes Tensorflow 1.6 without AVX

Tensorflow 1.6

```
git clone https://github.com/tensorflow/tensorflow/releases/tag/v1.6.0

cd tensorflow-1.6.0/
```

Tensoflow 1.8

```
git clone https://github.com/tensorflow/tensorflow/releases/tag/v1.8.0

cd tensorflow-1.8.0/
```

Once your desired source files are downloaded and the directory has been navigated to run

```
./configure
```

This will start an interactive configuration

- You will likely be using the defaul python paths
- Enter '-march=native' for the appropriate optimisation flags for the computer you are building on
- The other options should all be answered no for a default CPU configuration

Now you need to build and export the pip package that you will install

```
bazel build --config=opt //tensorflow/tools/pip_package:build_pip_package

bazel-bin/tensorflow/tools/pip_package/build_pip_package /path/to/the/built/.whl
```

This .whl can now be used with pip to install your custom Tensorflow install

```
sudo pip install /path/to/the/built/.whl/tensorflow-1.x.x-py2-none-any.whl
```

