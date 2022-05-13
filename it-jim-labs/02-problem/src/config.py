import torch
from pathlib import Path


class Config:
    def __init__(self):
        self.path_to_root = Path('..')
        self.path_to_data = self.path_to_root / 'data'
        self.path_to_output = self.path_to_root / 'output'
        self.path_to_models = self.path_to_output / 'models'
        self.path_to_predictions = self.path_to_output / 'predictions'
        self.path_to_tensorboard_logs = self.path_to_output / 'tensorboard_logs'
        
        self.classes = ('daisy', 'dandelion', 'roses', 'sunflowers', 'tulips')
        self.class_to_idx = {label: idx for idx, label in enumerate(self.classes)}
        self.idx_to_class = {idx: label  for idx, label in enumerate(self.classes)}
        self.validation_ratio = 0.2
        self.shuffle = True
        self.use_stratify = True
        
        self.start_epoch = 0
        self.epochs = 10
        self.batch_size = 32
        self.num_workers = 4
        self.pin_memory = True
        self.use_gpu = True
        self.device = f"cuda:{torch.cuda.current_device()}" if self.use_gpu and torch.cuda.is_available() else "cpu"
        self.seed = 42
        self.print_freq = 10
        
        self.use_descriptors_as_features = True
        
        if self.use_descriptors_as_features:
            self.features_type = 'lbp'
            
            self.lr = 3e-3
            
            self.img_height = 224
            self.img_width = 224
            self.norm_mean = None
            self.norm_std = None
        else:
            self.features_type = None
            self.encoder_name = 'resnet18'
            self.pretrained = True
            self.lr = 3e-4
            
            self.img_height = 224
            self.img_width = 224
            self.norm_mean = [0.485, 0.456, 0.406]
            self.norm_std = [0.229, 0.224, 0.225]
        
        self._init_dirs()
        
    def _init_dirs(self):
        self.path_to_data.mkdir(exist_ok=True)
        self.path_to_output.mkdir(exist_ok=True)
        self.path_to_models.mkdir(exist_ok=True)
        self.path_to_predictions.mkdir(exist_ok=True)
        self.path_to_tensorboard_logs.mkdir(exist_ok=True)
        
        
opt = Config()
