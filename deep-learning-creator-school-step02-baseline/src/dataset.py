import torch
import numpy as np
import cv2
import glob
from torch.utils.data import Dataset


class FaceDataset(Dataset):
    def __init__(self, img_dirs, labels, n_faces=1, preprocess=None):
        self.img_dirs = img_dirs
        self.labels = labels
        self.n_faces = n_faces
        self.preprocess = preprocess

    def __len__(self):
        return len(self.img_dirs)
    
    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        img_dir = self.img_dirs[idx]
        label = self.labels[idx]
        face_paths = glob.glob(f'{img_dir}/*.png')

        if len(face_paths) >= self.n_faces:
            sample = sorted(np.random.choice(face_paths, self.n_faces, replace=False))
        else:
            sample = sorted(np.random.choice(face_paths, self.n_faces, replace=True))
            
        faces = []
        for face_path in sample:
            face = cv2.imread(face_path, 1)
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            faces.append(face)
            
        if self.preprocess is not None:
            d = {f'image{i-1}': faces[i] for i in range(1, self.n_faces)}
            d['image'] = faces[0]
            preprocess_imgs = self.preprocess(**d)
            faces = [preprocess_imgs[f'image{i-1}'] for i in range(1, self.n_faces)]

        return {'faces': torch.stack(faces).permute(1, 0, 2, 3), 'label': torch.tensor([label], dtype=torch.float)}#{'faces': np.concatenate(faces, axis=-1).transpose(2, 0, 1), 'label': np.array([label], dtype=float)}
        