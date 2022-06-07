import torch.nn as nn
from apex import amp

from utils.apex_utils import get_dataloaders, train_model, init_model

FP16_TRAIN = True

dataloaders, dataset_sizes, class_names = get_dataloaders(data_dir='hymenoptera_data')
criterion = nn.CrossEntropyLoss()

if not FP16_TRAIN:
    # 859 Mb memory consumption on 1060
    model_fp32, optimizer_fp32, exp_lr_scheduler = init_model(len(class_names))
    train_model(model_fp32, criterion, optimizer_fp32, exp_lr_scheduler, num_epochs=10, dataloaders=dataloaders, dataset_sizes=dataset_sizes)

else:
    # 659 Mb memory consumption on 1060
    model, optimizer, exp_lr_scheduler = init_model(len(class_names))
    model_fp16, optimizer_fp16 = amp.initialize(model, optimizer, opt_level='O2', keep_batchnorm_fp32=True)
    train_model(model_fp16, criterion, optimizer_fp16, exp_lr_scheduler, num_epochs=10, dataloaders=dataloaders, dataset_sizes=dataset_sizes)
