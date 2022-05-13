import albumentations as A
import albumentations.augmentations.transforms as T
from albumentations.pytorch import ToTensorV2
from config import opt


train_transformations = A.Compose([
    A.Rotate(limit=45, p=0.3),
    A.OneOf([
        A.Compose([
            A.Resize(256, 256, p=1),
            A.RandomCrop(opt.img_height, opt.img_width, p=1),
        ], p=1),
        A.Resize(opt.img_height, opt.img_width, p=1),
    ], p=1),
    
    A.HorizontalFlip(p=0.5),
    
    A.OneOf([
        A.RandomBrightnessContrast(brightness_limit=0.4, contrast_limit=0.4, p=0.9),
        A.HueSaturationValue(hue_shift_limit=20, sat_shift_limit=30, val_shift_limit=20, p=0.9),
        T.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1, hue=0.1, p=0.9),
    ], p=0.3),
    
    T.Downscale(scale_min=0.25, scale_max=0.25, interpolation=0, p=0.1),
    T.ISONoise(color_shift=(0.01, 0.05), intensity=(0.1, 0.5), p=0.1),
    
    A.OneOf([
        T.ToSepia(p=1),
        T.ToGray(p=1),
    ], p=0.2),
    
    A.OneOf([
        A.GaussianBlur(blur_limit=(5, 5), p=0.9),
        A.MedianBlur(blur_limit=5, p=0.9),
        T.MotionBlur(blur_limit=5, p=0.9),
    ], p=0.3),
        
    
    A.Normalize(mean=opt.norm_mean, std=opt.norm_std, p=1),
    ToTensorV2(),
])

val_transformations = A.Compose([
    A.Resize(opt.img_height, opt.img_width, p=1),
    A.Normalize(mean=opt.norm_mean, std=opt.norm_std, p=1),
    ToTensorV2()
])

train_transformations_without_norm = A.Compose([
    A.Rotate(limit=45, p=0.3),
    A.OneOf([
        A.Compose([
            A.Resize(256, 256, p=1),
            A.RandomCrop(opt.img_height, opt.img_width, p=1),
        ], p=1),
        A.Resize(opt.img_height, opt.img_width, p=1),
    ], p=1),
    
    A.HorizontalFlip(p=0.5),
    
    A.OneOf([
        A.RandomBrightnessContrast(brightness_limit=0.4, contrast_limit=0.4, p=0.9),
        A.HueSaturationValue(hue_shift_limit=20, sat_shift_limit=30, val_shift_limit=20, p=0.9),
        T.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1, hue=0.1, p=0.9),
    ], p=0.3),
    
    T.Downscale(scale_min=0.25, scale_max=0.25, interpolation=0, p=0.1),
    T.ISONoise(color_shift=(0.01, 0.05), intensity=(0.1, 0.5), p=0.1),
    
    A.OneOf([
        T.ToSepia(p=0.9),
        T.ToGray(p=0.9),
    ], p=0.2),
    
    A.OneOf([
        A.GaussianBlur(blur_limit=(5, 5), p=0.9),
        A.MedianBlur(blur_limit=5, p=0.9),
        T.MotionBlur(blur_limit=5, p=0.9),
    ], p=0.2),
        
    ToTensorV2(),
])

val_transformations_without_norm = A.Compose([
    A.Resize(opt.img_height, opt.img_width, p=1),
    ToTensorV2()
])
