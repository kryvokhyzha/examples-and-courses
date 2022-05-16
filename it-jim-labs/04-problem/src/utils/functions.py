import shutil
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (16, 9)

import torch
from torch.utils.data.sampler import SubsetRandomSampler
from torchvision.utils import make_grid
from torchvision.datasets import MNIST

from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from config import opt


def get_dataloaders(train_disc_transformations, val_disc_transformations, train_autoenc_transformations, val_autoenc_transformations, target_transform):
    train_autoencoder_dataset = MNIST(
        opt.path_to_data / 'mnist', download=True, train=True,
        transform=train_autoenc_transformations,
        target_transform=target_transform,
    )
    val_autoencode_dataset = MNIST(
        opt.path_to_data / 'mnist', download=True, train=False,
        transform=val_autoenc_transformations,
        target_transform=target_transform,
    )
    
    train_disc_dataset = MNIST(
        opt.path_to_data / 'mnist', download=True, train=True,
        transform=train_disc_transformations,
        target_transform=target_transform,
    )
    val_disc_dataset = MNIST(
        opt.path_to_data / 'mnist', download=True, train=False,
        transform=val_disc_transformations,
        target_transform=target_transform,
    )
    
    train_autoencoder_sampler, train_disc_sampler = get_samplers(train_autoencoder_dataset, opt.autoencoder_data_ratio, opt.shuffle, opt.seed)
    val_autoencoder_sampler, val_disc_sampler = get_samplers(val_autoencode_dataset, opt.autoencoder_data_ratio, opt.shuffle, opt.seed)
    
    train_autoencoder_loader = torch.utils.data.DataLoader(
        train_autoencoder_dataset, batch_size=opt.batch_size, sampler=train_autoencoder_sampler,
        shuffle=False, num_workers=opt.num_workers, pin_memory=opt.pin_memory,
    )
    val_autoencoder_loader = torch.utils.data.DataLoader(
        val_autoencode_dataset, batch_size=opt.batch_size, sampler=val_autoencoder_sampler,
        shuffle=False, num_workers=opt.num_workers, pin_memory=opt.pin_memory,
    )
    
    train_disc_loader = torch.utils.data.DataLoader(
        train_disc_dataset, batch_size=opt.batch_size, sampler=train_disc_sampler,
        shuffle=False, num_workers=opt.num_workers, pin_memory=opt.pin_memory,
    )
    val_disc_loader = torch.utils.data.DataLoader(
        val_disc_dataset, batch_size=opt.batch_size, sampler=val_disc_sampler,
        shuffle=False, num_workers=opt.num_workers, pin_memory=opt.pin_memory,
    )
    
    return train_autoencoder_loader, val_autoencoder_loader, train_disc_loader, val_disc_loader
        

def get_samplers(dataset, data_ratio, shuffle, seed):
    dataset_size = len(dataset)
    indices = list(range(dataset_size))
    split = int(np.floor(data_ratio * dataset_size))
    
    if shuffle:
        np.random.seed(seed)
        np.random.shuffle(indices)
    indices1, indices2 = indices[split:], indices[:split]
    sampler1 = SubsetRandomSampler(indices1)
    sampler2 = SubsetRandomSampler(indices2)
    return sampler1, sampler2


def show_tensor_images(image_tensor, norm_mean=None, norm_std=None, num_images=8, nrow=4, add_noise=False):
    image_unflat = image_tensor.detach().cpu()
    image_grid = make_grid(image_unflat[:num_images], nrow=nrow)
    image_grid = image_grid[0].unsqueeze(0)
    image_grid = image_grid.permute(1, 2, 0)
    
    if norm_mean is not None and norm_std is not None:
        mean = torch.FloatTensor(norm_mean)
        std = torch.FloatTensor(norm_std)
        image_grid = image_grid.mul(std).add(mean)
    if add_noise:
        image_grid = add_gaussian_noise(image_grid)
    plt.imshow(image_grid.squeeze(), cmap='gray')
    
    
def save_checkpoint(state, is_best, filename='checkpoint.pth', best_filename='model_best.pth'):
    torch.save(state, filename)
    if is_best:
        shutil.copyfile(filename, best_filename)
        
    
def adjust_learning_rate(optimizer, epoch, lr):
    """Sets the learning rate to the initial LR decayed by 10 every 30 epochs"""
    lr = lr * (0.1 ** (epoch // 30))
    for param_group in optimizer.param_groups:
        param_group['lr'] = lr


def accuracy(output, target):
    t1 = torch.argmax(target, dim=1).detach().cpu().numpy()
    t2 = torch.argmax(output, dim=1).detach().cpu().numpy()
    return accuracy_score(t1, t2)


def f1(output, target):
    t1 = torch.argmax(target, dim=1).detach().cpu().numpy()
    t2 = torch.argmax(output, dim=1).detach().cpu().numpy()
    return f1_score(t1, t2, average='weighted')


def precision(output, target):
    t1 = torch.argmax(target, dim=1).detach().cpu().numpy()
    t2 = torch.argmax(output, dim=1).detach().cpu().numpy()
    return precision_score(t1, t2, average='weighted')


def recall(output, target):
    t1 = torch.argmax(target, dim=1).detach().cpu().numpy()
    t2 = torch.argmax(output, dim=1).detach().cpu().numpy()
    return recall_score(t1, t2, average='weighted')


def add_gaussian_noise(image_tensor, noise_factor=0.5):
    noise_image_tensor  = torch.clip(image_tensor + torch.randn_like(image_tensor) * noise_factor, 0., 1.)
    return noise_image_tensor


def init_seeds(seed):
    import random
    import numpy as np
    import torch
    random.seed(seed)
    np.random.seed(seed)
    torch.backends.cudnn.enabled = False
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
