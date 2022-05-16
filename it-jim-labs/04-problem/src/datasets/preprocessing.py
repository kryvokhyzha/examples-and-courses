import torch
import torchvision.transforms as T
from config import opt


class TargetTransform:
    def __init__(self):
        pass

    def __call__(self, x):
        target = torch.zeros(size=(opt.n_classes,))
        target[x] = 1.0
        target = torch.FloatTensor(target)
        return target


train_autoencoder_transformations = T.Compose([
    T.RandomRotation(degrees=(-45, 45)),
    T.ToTensor(),
])

val_autoencoder_transformations = T.Compose([
    T.ToTensor(),
])

train_disc_transformations = T.Compose([
    T.RandomRotation(degrees=(-45, 45)),
    T.ToTensor(),
])

val_disc_transformations = T.Compose([
    T.ToTensor(),
])

target_transform = T.Compose([
    T.Lambda(TargetTransform()),
])
