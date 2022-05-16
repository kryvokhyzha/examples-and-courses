# Problem 2

You have to implement **an image classification neural network** for the [FLOWERS dataset](https://drive.google.com/file/d/1OxuNIvlJ6FLWtS5POvJv54Dm0Gj8wqAv/view?usp=sharing). Feel free to reduce the number of examples for each class in your dataset if training on your hardware takes too much time.

For this task, you should make at least **two neural networks**: a fully connected one that works on top of some extracted classic features/descriptors (histograms, Gabor, HOG, etc.) and a convolutional one with class prediction at the end. In the code you can propose a few alternative architectures and pick the best among them.

You can do it either in Keras or Pytorch. It's better to do both.

As an **output**, you should provide your **code, trained model files** (2 pcs. at least), and a brief report with standard **metrics** for classifiers (confusion matrix, precision, recall, F1 score) [calculated on test images].

Your code should provide **3 execution modes/functions: train** (for training new model), **test** (for testing the trained and saved model on the test dataset), and **infer** (for inference on a particular folder with images or a single image).

## Project structure

```
02-problem
│   README.md
│   .gitignore
│
└───data (contains train/val/test data)
│   └───daisy
│       │   5547758_eea9edfd54_n.jpg
│       │   5673551_01d1ea993e_n.jpg
│       │   ...
│   └───...
│       │   ...
│   
└───output (contains best models and training logs)
│   └───models
│       │   FlowersConvModel_model_best.pth
│       │   FlowersFcModel_model_best.pth
│       │   ...
│   └───tensorboard_logs
│       └───FlowersConvModel
│           │   ...
│       └───FlowersFcModel
│           │   ...
└───src (contains source code and notebooks with report)
│   config.py
│   01-fc-model-run.ipynb
│   02-conv-model-run.ipynb
│
│   └───models
│       │   __init__.py
│       │   flowers_dataset.py
│       │   preprocessing.py
│   └───models
│       │   __init__.py
│       │   model_conv.py
│       │   model_fc.py
│   └───utils
│       │   __init__.py
│       │   functions.py
│       │   loops.py
│       │   meters.py
```

## Task 1 - FC model

+ Build a simple fully connected model
+ HOG and LBP were used to extract features from image
+ Weights for best models are in `output/models`
+ Tensorboard logs are in `output/tensorboard_logs`
+ [Report notebook](https://github.com/kryvokhyzha/examples-and-courses/tree/master/it-jim-labs/02-problem/src/01-fc-model-run.ipynb) - `src/01-fc-model-run.ipynb`

## Task 2 - Conv model

+ As a model I use pretrained `resnet-18`
+ This model is chosen in terms of the balance between learning speed and model quality
+ Yes, it's possible to use pretrained `ViT`, `resnet-101` or something larger, but to my mind it is **overkill** for this task
+ Finetuning it's a powerful technique, but let's train model, passing the gradient through entire network and learning all possible weights, because of small size of our model
+ Weights for best models are in `output/models`
+ Tensorboard logs are in `output/tensorboard_logs`
+ [Report notebook](https://github.com/kryvokhyzha/examples-and-courses/tree/master/it-jim-labs/02-problem/src/02-conv-model-run.ipynb) - `src/02-conv-model-run.ipynb`

## Possible ways to improve speed or model performance

+ Try others descriptors and specific features
+ Simplify fully connected model architecture
+ Compress the model using ONNX format and create inference session
