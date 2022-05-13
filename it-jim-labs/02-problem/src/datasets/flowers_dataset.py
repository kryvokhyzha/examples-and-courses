import cv2
import numpy as np
import torch
from skimage.feature import hog, local_binary_pattern
from torch.utils.data import Dataset


class FlowersDataset(Dataset):
    def __init__(self, img_paths, labels=None, num_classes=1, transform=None, use_descriptors_as_features=False, features_type='hog'):
        self.img_paths = img_paths
        self.labels = labels
        self.num_classes = num_classes
        self.transform = transform
        self.use_descriptors_as_features = use_descriptors_as_features
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
            if self.features_type == 'hog':
                image = FlowersDataset._get_hog_features(image)
            elif self.features_type == 'lbp':
                image = FlowersDataset._get_lbp_features(image)
            elif self.features_type == 'lbp+hog':
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
    def _get_features(image):
        lbp_f = FlowersDataset._get_lbp_features(image)
        hog_f = FlowersDataset._get_hog_features(image)
        features = np.concatenate([lbp_f, hog_f], axis=0)
        return features
    
    @staticmethod
    def _get_gabor_features(image, filters=None):
        if filters is None:
            filters = FlowersDataset._build_gabor_filters()
        features = FlowersDataset._process_gabor(cv2.cvtColor(image, cv2.COLOR_RGB2GRAY), filters).flatten()
        features = (features / 127.5) - 1.0
        return features
    
    @staticmethod
    def _get_hog_features(image):
        features = FlowersDataset._process_hog(image)
        features = (features / 127.5) - 1.0
        return features
    
    @staticmethod
    def _get_lbp_features(image):
        features = FlowersDataset._process_lbp(cv2.cvtColor(image, cv2.COLOR_RGB2GRAY))
        return features
  
  
    @staticmethod
    def _build_gabor_filters():
        filters = []
        ksize = 31
        for theta in np.arange(0, np.pi, np.pi / 16):
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
        def compute(orientations=9, pixels_per_cell=(8, 8), cells_per_block=(3, 3)):
            features = hog(
                img, orientations=orientations, pixels_per_cell=pixels_per_cell,
                cells_per_block=cells_per_block, visualize=False, multichannel=True,
                feature_vector=True,
            )
            return features
        
        features = np.concatenate([
            compute(orientations=19, pixels_per_cell=(64, 64), cells_per_block=(3, 3)),
            compute(orientations=29, pixels_per_cell=(96, 96), cells_per_block=(3, 3)),
        ], axis=0)
        return features
    
    @staticmethod
    def _process_lbp(img):
        def compute(numPoints, radius, eps=1e-7):
            lbp = local_binary_pattern(img, numPoints, radius, method="uniform")
            features, _ = np.histogram(
                lbp.ravel(),
                bins=np.arange(0, numPoints + 3),
                range=(0, numPoints + 2)
            )
            # normalize the histogram
            features = features.astype("float")
            features /= (features.sum() + eps)
            return features
        
        features = np.concatenate([
            compute(numPoints=512, radius=11),
            compute(numPoints=512, radius=51),
            compute(numPoints=512, radius=96),
        ], axis=0)
        return features
