from pathlib import Path
import cv2


class Config:
    def __init__(self):
        self.path_to_root = Path('..')
        self.path_to_data = self.path_to_root / 'data'
        self.path_to_output = self.path_to_root / 'output'
        self.path_to_predictions = self.path_to_output / 'predictions'
        
        self.input_video_name = 'find_chocolate.mp4'
        self.input_marker_img_name = 'marker.jpg'
        
        self.n_features = 10000
        self.min_match_cnt = 5
        self.cutoff_coef = 3
        self.nn_match_ratio = 0.8
        
        # self.detect_interval = 50
        self.lk_params = dict(
            winSize=(15, 15),
            maxLevel=2,
            criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
        )
        
        self._init_dirs()
        
    def _init_dirs(self):
        self.path_to_data.mkdir(exist_ok=True)
        self.path_to_output.mkdir(exist_ok=True)
        self.path_to_predictions.mkdir(exist_ok=True)
        
        
opt = Config()
