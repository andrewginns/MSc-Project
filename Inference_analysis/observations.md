# Observations
Notes about the different models and their characteristics

## optimized-graph.pb
* Huge reduction in size compared to the base frozen-graph.pb
* Inference speed is not affected in a significant way

## float.tflite
* Due to the use of floating point calculations the model size has not been reduced much
* Inference speed is almost an order of magnitude slower on the Pixel 2XL and about 5x slower on desktop hardware
* Likely due to the format inefficiencies of floating point calculations due to the TFLite framwork