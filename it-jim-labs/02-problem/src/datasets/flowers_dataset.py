import cv2
import numpy as np
import torch
from skimage.feature import hog
from torch.utils.data import Dataset


class FlowersDataset(Dataset):
    def __init__(self, img_paths, labels=None, num_classes=1, transform=None, use_descriptors_as_features=False, features_type='hog'):
        self.img_paths = img_paths
        self.labels = labels
        self.num_classes = num_classes
        self.transform = transform
        self.use_descriptors_as_features = use_descriptors_as_features
        self.gabor_filters = FlowersDataset._build_gabor_filters()
        self.features_type = features_type

    def __len__(self):
        return len(self.img_paths)
    
    def __getitem__(self, idx):
        img_path = self.img_paths[idx]
        
        image = cv2.imread(img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        if self.transform is not None:
            image = self.transform(image=image)['image']
            
        if self.use_descriptors_as_features:
            image = image.permute(1, 2, 0).detach().cpu().numpy()
            if self.features_type == 'gabor':
                image = FlowersDataset._get_gabor_features(image, self.gabor_filters)
            elif self.features_type == 'hog':
                image = FlowersDataset._get_hog_features(image)
            elif self.features_type == 'hog+gabor':
                image = FlowersDataset._get_features(image)
            else:
                raise NotImplementedError()
            image = torch.FloatTensor(image)
            
        if self.labels is not None:
            label = self.labels[idx]
            if self.num_classes > 1:
                target = torch.zeros(size=(self.num_classes,))
                target[label] = 1.0
                target = torch.FloatTensor(target)
            else:
                target = torch.FloatTensor([label])
        else:
            target = None

        return {'image': image, 'target': target}
    
    @staticmethod
    def _get_features(image, filters=None):
        gabor_f = FlowersDataset._get_gabor_features(image, filters)
        hog_f = FlowersDataset._get_hog_features(image)
        features = np.concatenate([gabor_f, hog_f], axis=0)
        return features
    
    @staticmethod
    def _get_gabor_features(image, filters=None):
        if filters is None:
            filters = FlowersDataset._build_gabor_filters()
        features = FlowersDataset._process_gabor(image, filters).flatten()
        features = (features / 127.5) - 1.0
        return features
    
    @staticmethod
    def _get_hog_features(image):
        features = FlowersDataset._process_hog(image)
        features = (features / 127.5) - 1.0
        return features
    
    @staticmethod
    def _build_gabor_filters():
        filters = []
        ksize = 31
        for theta in np.arange(0, np.pi, np.pi / 4):
            kern = cv2.getGaborKernel((ksize, ksize), 4.0, theta, 10.0, 0.5, 0, ktype=cv2.CV_32F)
            kern /= 1.5*kern.sum()
            filters.append(kern)
        return filters

    @staticmethod
    def _process_gabor(img, filters):
        accum = np.zeros_like(img)
        for kern in filters:
            fimg = cv2.filter2D(img, cv2.CV_8UC3, kern)
            np.maximum(accum, fimg, accum)
        return accum
    
    @staticmethod
    def _process_hog(img):
        features = hog(
            img, orientations=32, pixels_per_cell=(16, 16),
            cells_per_block=(4, 4), visualize=False, multichannel=True,
            feature_vector=True,
        )
        return features
