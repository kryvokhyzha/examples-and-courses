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
        
        self.autoencoder_data_ratio = 0.5
        self.shuffle = True
        self.use_stratify = True
        
        self.start_epoch = 0
        self.epochs = 15
        self.batch_size = 128
        self.num_workers = 4
        self.pin_memory = True
        self.use_gpu = True
        self.device = f"cuda:{torch.cuda.current_device()}" if self.use_gpu and torch.cuda.is_available() else "cpu"
        self.seed = 42
        self.print_freq = 10
        
        self.disc_hidden_channels = 16
        self.autoencoder_hidden_channels = 16
        self.encoder_out_channels = self.autoencoder_hidden_channels * 8
        
        self.lr = 3e-4
        
        self.n_classes = 10
        self.img_height = 28
        self.img_width = 28
        self.norm_mean = None
        self.norm_std = None
        
        self._init_dirs()
        
    def _init_dirs(self):
        self.path_to_data.mkdir(exist_ok=True)
        self.path_to_output.mkdir(exist_ok=True)
        self.path_to_models.mkdir(exist_ok=True)
        self.path_to_predictions.mkdir(exist_ok=True)
        self.path_to_tensorboard_logs.mkdir(exist_ok=True)
        
        
opt = Config()
