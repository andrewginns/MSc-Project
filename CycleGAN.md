# Network Architecture
We adapt the architecture for our generative networks from Johnson et al. [22] who have shown impressive results for neural style transfer and super-resolution. This network contains two stride-2 convolutions, several residual blocks [17], and two fractionally strided convolutions with stride 1 . We use 6 blocks for 2 128 × 128 images, and 9 blocks for 256 × 256 and higher- resolution training images. Similar to Johnson et al. [22], we use instance normalization [52]. For the discriminator networks we use 70 × 70 PatchGANs [21, 28, 27], which aim to classify whether 70 × 70 overlapping image patches are real or fake. Such a patch-level discriminator architec- ture has fewer parameters than a full-image discriminator, and can be applied to arbitrarily-sized images in a fully convolutional fashion [21]. https://arxiv.org/pdf/1703.10593.pdf

## Generator
Conv2D
FusedBatchNorm
Const
Conv2dBackpropInput
Relu
Add
BiasAdd
StridedSlice
NoOp
Tanh
Mul
Pack
Retval
Arg
Shape

## Discriminator

## Image handling
The network expects RGB images normalised to [-1.0,1.0] as input to the network. The python program for training and inference uses scipy's imread to accomplish this.
~~~~
scipy.misc.imread(path, mode=mode) / 127.5 - 1
~~~~
The image loaded into the network is a float64 RGB image [-1.0, 1] with 3 values per pixel corresponding to the three colour channels.

The output from the network is in the same format, float64 RGB [-1.0, 1]. The python program converts this to [0, 255] as an unsigned int8 using imsave.
~~~~
scipy.misc.imsave(path, _to_range(image, 0, 255, np.uint8))
~~~~