# Problem 4

You should train your own autoencoder that will denoise handwritten digits in the MNIST dataset. As an input, you should feed images corrupted by some well-visible noise. At the output, you should get the denoised image.
To evaluate the effectiveness of the denoising you should train a simple classification network trained on a standard dataset and then evaluate it on three types of input:

+ standard test set
+ noisy test set
+ denoised test set

If everything is done right, the accuracy on denoised images should be close to the one on a normal dataset. Please, use the standard built-in MNIST dataset of PyTorch and Tensorflow/Keras.

Deliverables for this task:

+ code that has functions for training and inference of an autoencoder on a single image
+ trained autoencoder model
+ visualization of results
+ optionally [will be a plus]: classification metrics (at least an accuracy) on three versions of the test set (clean, noisy and denoised).

## Project structure

```
04-problem
│   README.md
│   .gitignore
│
└───data (contains standart built-in MNIST dataset)
│   └───mnist
│       │   ...
│   
└───output (contains best models and training logs)
│   └───models
│       │   DenoiserMNISTModel_model_best.pth
│       │   DiscMNISTModel_model_best.pth
│       │   ...
│   └───tensorboard_logs
│       └───DenoiserMNISTModel
│           │   ...
│       └───DiscMNISTModel
│           │   ...
│
└───src (contains source code and notebooks with report)
│   config.py
│   01-train-discriminator.ipynb
│   02-train-autoencoder.ipynb
│   03-report.ipynb
│
│   └───datasets
│       │   __init__.py
│       │   preprocessing.py
│   └───models
│       │   __init__.py
│       │   autoencoder.py
│       │   discriminator.py
│   └───utils
│       │   __init__.py
│       │   functions.py
│       │   loops.py
│       │   meters.py
```

## Solution

+ Weights for best models are in `output/models`
+ Tensorboard logs are in `output/tensorboard_logs`
+ [Report notebook](https://github.com/kryvokhyzha/examples-and-courses/tree/master/it-jim-labs/04-problem/src/03-report.ipynb) - `src/03-report.ipynb`
+ example of noised data
![noised-data](https://github.com/kryvokhyzha/examples-and-courses/tree/master/it-jim-labs/04-problem/assets/noised-data.png)
+ example of data denoising
![denoised-data](https://github.com/kryvokhyzha/examples-and-courses/tree/master/it-jim-labs/04-problem/assets/denoised-data.png)
+ metrics on validation set without noise
        + Accuracy: 0.965
        + F1: 0.965
        + Precision: 0.966
        + Recall: 0.965
        ![denoised-data](https://github.com/kryvokhyzha/examples-and-courses/tree/master/it-jim-labs/04-problem/assets/val-without-noise.png)
+ metrics on validation set with noise
        + Accuracy: 0.909
        + F1: 0.909
        + Precision: 0.91
        + Recall: 0.909
        ![denoised-data](https://github.com/kryvokhyzha/examples-and-courses/tree/master/it-jim-labs/04-problem/assets/val-with-noise.png)
+ metrics on denoised validation set
        + Accuracy: 0.938
        + F1: 0.938
        + Precision: 0.939
        + Recall: 0.938
        ![denoised-data](https://github.com/kryvokhyzha/examples-and-courses/tree/master/it-jim-labs/04-problem/assets/denoised-val.png)
