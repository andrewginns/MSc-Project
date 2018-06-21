# Network Architecture
We adapt the architecture for our generative networks from Johnson et al. [22] who have shown impressive results for neural style transfer and super-resolution. This network contains two stride-2 convolutions, several residual blocks [17], and two fractionally strided convolutions with stride 1 . We use 6 blocks for 2 128 × 128 images, and 9 blocks for 256 × 256 and higher- resolution training images. Similar to Johnson et al. [22], we use instance normalization [52]. For the discriminator networks we use 70 × 70 PatchGANs [21, 28, 27], which aim to classify whether 70 × 70 overlapping image patches are real or fake. Such a patch-level discriminator architec- ture has fewer parameters than a full-image discriminator, and can be applied to arbitrarily-sized images in a fully convolutional fashion [21]. https://arxiv.org/pdf/1703.10593.pdf

## Generator

## Discriminator
