import torch
import shutil
import numpy as np

from torch.utils.data import DataLoader
from torchvision import models
from facenet_pytorch import MTCNN
from albumentations import Normalize, Compose, Resize, CenterCrop
from albumentations.pytorch import ToTensorV2
from tqdm import tqdm

from config import opt
from face_extractor import FaceExtractor, compute_face_extractor
from dataset import FaceDataset
from model import DeepfakeClassifierR3D18


test_transforms = Compose([
        Resize(opt.H + opt.delta, opt.W + opt.delta),
        CenterCrop(opt.H, opt.W),
        Normalize(mean=opt.mean, std=opt.std, p=1),
        ToTensorV2()
    ], additional_targets={f'image{i}': 'image' for i in range(0, opt.n_faces-1)}
)


def prepare_images(path_to_video, path_to_output_images):
    # Load face detector
    face_detector = MTCNN(margin=14, keep_all=True, factor=0.5, device=opt.device).eval()
    
    # Define face extractor
    face_extractor = FaceExtractor(detector=face_detector, n_frames=opt.n_frames)
    
    with torch.no_grad():
        compute_face_extractor(face_extractor, str(path_to_video), str(path_to_output_images))
        
        
def prepare_dataloader(img_dir):
    test_dataset = FaceDataset(
        img_dirs=np.asarray([img_dir]),
        labels=[0],
        n_faces=opt.n_faces,
        preprocess=test_transforms
    )
    
    test_dataloader = DataLoader(
        test_dataset,
        batch_size=opt.batch_size,
        shuffle=False,
        num_workers=opt.num_workers,
    )
    
    return test_dataloader


def prepare_model(path_to_weights):
    encoder_r3d_18 = models.video.r3d_18()
    
    classifier = DeepfakeClassifierR3D18(encoder=encoder_r3d_18, linear_size=512, num_classes=1)
        
    state = torch.load(path_to_weights, map_location=lambda storage, loc: storage)
    classifier.load_state_dict(state['state_dict'])
    
    return classifier.to(opt.device).eval()
    
    
    
def inference(classifier, test_dataloader):
    classifier.eval()
    
    all_preds = []
    all_labels = []
    with torch.no_grad():
        for _, batch in enumerate(tqdm(test_dataloader, total=len(test_dataloader))):
            # Make prediction.
            y_pred = classifier(batch['faces'].to(opt.device))

            all_preds.extend(y_pred.squeeze(dim=-1).detach().cpu().numpy().tolist())
            all_labels.extend(batch['label'].squeeze(dim=-1).numpy().tolist())
    return all_preds, all_labels
    
    
if __name__ == '__main__':
    torch.manual_seed(opt.seed)
    np.random.seed(opt.seed)
    
    path_to_video = opt.path_to_assets / 'test-video.mp4'
    filename = str(path_to_video).split('/')[-1].split('.')[0]
    
    prepare_images(path_to_video, opt.path_to_output_images)
    output_imgs_dir = str(opt.path_to_output_images / filename)
    test_dataloader = prepare_dataloader(output_imgs_dir)

    classifier = prepare_model(opt.path_to_models / f'{str(opt.model_name)}.pth')
    
    test_prediction, _ = inference(classifier, test_dataloader)
    print('Prediction length:', len(test_prediction))
    print('Prediction proba:', test_prediction)
    print('Prediction label:', [int(pred > opt.threshold) for pred in test_prediction])
    
    shutil.rmtree(output_imgs_dir)
    