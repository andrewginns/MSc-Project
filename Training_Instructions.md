# Training Instructions

## Requirements for reproduction

- Tested on macOS 10.13 and Ubuntu 16.04.4
- Python 2.7.12
- Bazel 0.10.0 or 0.11.0 https://github.com/bazelbuild/bazel/releases
- Tensorflow 1.6 installed (GPU enabled build recommended for training)
- CycleGAN code from https://github.com/andrewginns/CycleGAN-Tensorflow-PyTorch

## Training the network

1. Navigate to the directory and download training sets

```
cd $HOME/path/to/CycleGAN-Tensorflow-PyTorch

chmod +x ./download_dataset.sh

./download_dataset.sh summer2winter_yosemite
```

2. Run the network training
   * CUDA_VISIBLE_DEVICES=id used to specify the GPU ID to use

```
CUDA_VISIBLE_DEVICES=0 python train.py --dataset=summer2winter_yosemite
```

3. Collect the output files from outputs/checkpoints/dataset and outputs/summaries/dataset
4. Freeze the network into a graph file

```
python freeze.py --checkpoint_path=./outputs/checkpoints/dataset --output_nodes=a2b_generator/output_image --output_graph=/tmp/frozen-graph.pb
```