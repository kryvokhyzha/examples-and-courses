import os
import pandas as pd
import shutil
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (16, 9)

import torch
from torchvision.utils import make_grid

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score


def get_images_paths(opt, label_col='label'):
    data_df = []
    for label in opt.classes:
        images = os.listdir(opt.path_to_data / label)
        images = list(map(
            lambda x: str(opt.path_to_data / label / x),
            filter(lambda x: x.endswith('.jpg'), images)
        ))
        data_df.append({label_col: [opt.class_to_idx[label]] * len(images), 'path': images})
        
    return pd.concat([pd.DataFrame(x) for x in data_df]).reset_index(drop=True)


def get_train_test_split(df, opt, label_col='label'):
    df_train, df_test = train_test_split(
        df, test_size=opt.validation_ratio,
        random_state=opt.seed, shuffle=opt.shuffle,
        stratify=df[label_col] if opt.use_stratify else None,
    )
    return df_train, df_test


def show_tensor_images(image_tensor, norm_mean=None, norm_std=None, num_images=8, nrow=4):
    image_unflat = image_tensor.detach().cpu()
    image_grid = make_grid(image_unflat[:num_images], nrow=nrow)
    image_grid = image_grid.permute(1, 2, 0)
    
    if norm_mean is not None and norm_std is not None:
        mean = torch.FloatTensor(norm_mean)
        std = torch.FloatTensor(norm_std)
        image_grid = image_grid.mul(std).add(mean)
    plt.imshow(image_grid.squeeze())
    
    
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


def init_seeds(seed):
    import random
    import numpy as np
    import torch
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
