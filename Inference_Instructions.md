# Inference Instructions

## Requirements

* Tested on macOS 10.13 and Ubuntu 16.04.4
* CycleGAN code from https://github.com/andrewginns/CycleGAN-Tensorflow-PyTorch
* Python 2.7.12
* Trained model (.pb .ckpt .tflite)
* bazel 0.10.0 or 0.11.0 install
* For Edge node inference
  * Tensoflow 1.8+ source files
  * Android Studio: Android SDK level 27, Build tools 27.0.3, NDK version 15
  * CycleGAN Android app
    * CycleGAN Capture - Single image Style-Transfer <https://github.com/andrewginns/CycleGAN-Capture>
    * CycleGAN View - Live preview Style-Transfer <https://github.com/andrewginns/CycleGAN-TF-Android>
  * Movidius Neural Compute Stick (MNCS) 
    * Movidius Neural Compute SDK 2.04+ https://github.com/movidius/ncsdk/releases

## Desktop inference

Navigate to the CycleGAN directory root

Option 1: Using the checkpoint files (.ckpt)

```
python test.py --dataset=one_of_the_datasets
```

- Output images are from left to right: original image --> a2b --> b2a

```
python ckpt_a2b.py --checkpoints='/path/to/checkpoints.ckpt' --dataset='/path/to/images_folder'
```

- Output images are from left to right: original image --> a2b

Option 2: Using a model file (.pb)

```
python pb_a2b.py --graph='/path/to/.pb' --dataset='/path/to/image_folder'
```

- Output images are from left to right: original image --> a2b

## Edge node inference

Targetting:

- Android Devices with API level 27 (8.1 Oreo) and TF Lite 1.8
- Movidius Neural Compute Stick with Myriad 2 VPU and SDK 2.04

### Android Devices

Option 1: Using a model file (.pb)

1. Place a graph.pb file in the app directory 'android-app-name-here/android/assets'
2. Compile the project in Android Studio
3. Run on a device (real or virtual) connected through ADB

Option 2: Using a TFLite file (.tflite) **WIP**

1. Place a graph.tflite file in the app directory 'android-app-name-here/android/assets'
2. Compile the project in Android Studio
3. Run on a device (real or virtual) connected through ADB

### Movidius Neural Compute Stick

Convert to a Intel Movidius graph format - Ubuntu 16.04.4 required **WIP**

1. mvNCCompile /media/sf_vBox/optimized_graph.pb -in inputA -on a2b_generator/output_image