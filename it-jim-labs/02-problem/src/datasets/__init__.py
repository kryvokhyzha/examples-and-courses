import cv2
import torch
from .flowers_dataset import FlowersDataset

import warnings
warnings.filterwarnings("ignore")


def prepare_data_for_model(path_to_image, transform=None, use_descriptors_as_features=False, features_type='hog'):
    image = cv2.imread(path_to_image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    if transform is not None:
        image = transform(image=image)['image']
        
    if use_descriptors_as_features:
        image = image.permute(1, 2, 0).detach().cpu().numpy()
        if features_type == 'hog':
            image = FlowersDataset._get_hog_features(image)
        elif features_type == 'lbp':
            image = FlowersDataset._get_lbp_features(image)
        elif features_type == 'lbp+hog':
            image = FlowersDataset._get_features(image)
        else:
            raise NotImplementedError()
        
        image = torch.FloatTensor(image)
    
    return image.unsqueeze(0)
