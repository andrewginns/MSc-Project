# Bazel installation guide for windows
Based on official documentation https://docs.bazel.build/versions/master/windows.html#using

Reflective of an install on Windows 10 Spring Creators 1803 without a Visual Studio install

n.b. This bazel install isn't as capable as a Unix install. Some Tensorflow C++ tools will fail to compile due to type errors or similar

## Pre-requisites
* MSYS2 Shell http://www.msys2.org/
* Microsoft Visual C++ Redistributable for Visual Studio 2015 https://www.microsoft.com/en-us/download/details.aspx?id=48145
* Microsoft Visual Studio 2017 Build Tools https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2017

## Instructions
1. Download a windows bazel executable https://github.com/bazelbuild/bazel/releases
2. Rename the downloaded binary to bazel.exe and move it to a directory that's on your %PATH% or add its directory to your %PATH%
3. Open a new command window and type 'bazel' to test for a successful bazel environment install
4. Link the bazel environment to the C++ build tools. In the command window type 'set BAZEL_VS=C:\Program Files (x86)\Microsoft Visual Studio\2017\BuildTools'