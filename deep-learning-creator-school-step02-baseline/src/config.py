import torch
from pathlib import Path


class Config:
    def __init__(self):
        self.model_name = 'deep-fake-video-detection-model'
        
        self.path_to_root = Path('..')
        self.path_to_output = self.path_to_root / 'output'
        self.path_to_models = self.path_to_output / 'models'
        self.path_to_predictions = self.path_to_output / 'predictions'
        self.path_to_tensorboard_logs = self.path_to_output / 'tensorboard_logs'
        self.path_to_assets = self.path_to_root / 'assets'
        self.path_to_output_images = self.path_to_output / 'images'
        
        self.n_frames = 8
        self.n_faces = 6
        
        self.shuffle = True
        self.H, self.W = 112, 112
        self.delta = 10
        self.mean = [0.485, 0.456, 0.406]
        self.std = [0.229, 0.224, 0.225]
        self.threshold = 0.5
        self.epsilon = 1e-7
        
        self.batch_size = 32
        self.num_workers = 4
        self.pin_memory = False
        self.use_gpu = False
        
        try:
            if self.use_gpu and torch.has_mps:
                self.device = 'mps'
            else:
                self.device = f"cuda:{torch.cuda.current_device()}" if self.use_gpu and torch.cuda.is_available() else "cpu"
        except:
            self.device = f"cuda:{torch.cuda.current_device()}" if self.use_gpu and torch.cuda.is_available() else "cpu"
        
        self.seed = 42
        
        self._init_dirs()
        
    def _init_dirs(self):
        self.path_to_output.mkdir(exist_ok=True)
        self.path_to_models.mkdir(exist_ok=True)
        self.path_to_predictions.mkdir(exist_ok=True)
        self.path_to_tensorboard_logs.mkdir(exist_ok=True)
        self.path_to_assets.mkdir(exist_ok=True)
        self.path_to_output_images.mkdir(exist_ok=True)
        
        
opt = Config()
