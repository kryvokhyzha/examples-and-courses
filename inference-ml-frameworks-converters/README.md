# Convert PyTorch model to Portable ML frameworks

This repo contains a script to convert PyTorch MobileNetV2 model trained on Imagenet to inference frameworks like TorchMobile, ONNX, TFLite, and CoreML.
<b>NOTE</b>: you can perform inference of the CoreML model only in MacOS.

## Setup

```bash
pip install -r requirements.txt
```

## Run the conversion script

```bash
python3 run.py
```

## Assignment

1. Launch a `run.py` file to get checkpoints for all Portable ML frameworks, make sure that it works and you get valid predictions for the test image

2. Add some code to the bottom of the `main` function that evaluates the quality of conversion for different formats (with respect to the original PyTorch model) based on randomly generated inputs

3. It's up to you to select the metric for quality conversion

4. You can output metrics in any format: numbers, plots, etc

