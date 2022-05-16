import time
import torch
import numpy as np
import shutil
import matplotlib.pyplot as plt
from tensorboardX import SummaryWriter
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, confusion_matrix
from tqdm import tqdm
from torchvision.utils import make_grid
from datasets import prepare_data_for_disc_model, prepare_data_for_autoencoder_model
from utils.meters import AverageMeter, ProgressMeter
from utils.functions import accuracy, f1, precision, recall, save_checkpoint, add_gaussian_noise

import warnings
warnings.filterwarnings("ignore")


def train_disc_model(model, optimizer, scheduler, criterion, train_dataloader, val_dataloader, opt, target_metric='f1_avg', best_target_metric=-np.inf):
    model_writer_path = opt.path_to_tensorboard_logs / model.__class__.__name__

    if model_writer_path.exists():
        shutil.rmtree(model_writer_path)
    writer = SummaryWriter(log_dir=str(model_writer_path))

    for epoch in range(opt.start_epoch, opt.epochs):
        # train for one epoch
        _ = train_disc_one_epoch(train_dataloader, model, criterion, optimizer, epoch, opt.device, opt.print_freq, writer)

        # evaluate on validation set
        val_metrics = validate_disc_one_epoch(val_dataloader, model, criterion, epoch, opt.device, opt.print_freq, writer)
        
        # learning rate scheduler step
        scheduler.step(val_metrics['loss_avg'])

        # remember best value and save checkpoint
        target_metric_value = val_metrics[target_metric]
        is_best = target_metric_value > best_target_metric
        best_target_metric = max(target_metric_value, best_target_metric)

        save_checkpoint(
            {
                'epoch': epoch,
                'state_dict': model.state_dict(),
                f'best_{target_metric}': best_target_metric,
                'optimizer' : optimizer.state_dict(),
            },
            is_best,
            filename=str(opt.path_to_models / f'{model.__class__.__name__}_checkpoint.pth'),
            best_filename=str(opt.path_to_models / f'{model.__class__.__name__}_model_best.pth'),
        )
    writer.close()


def train_disc_one_epoch(train_loader, model, criterion, optimizer, epoch, device, print_freq, writer):
    batch_time = AverageMeter('Time', ':6.3f')
    data_time = AverageMeter('Data', ':6.3f')
    losse_meter = AverageMeter('Loss', ':.4e')
    accuracy_meter = AverageMeter('Acc', ':6.2f')
    f1_meter = AverageMeter('F1', ':6.2f')
    precision_meter = AverageMeter('PR', ':6.2f')
    recall_meter = AverageMeter('RC', ':6.2f')
    progress = ProgressMeter(
        len(train_loader),
        [batch_time, data_time, losse_meter, accuracy_meter, f1_meter],
        prefix=f"Epoch: [{epoch}]"
    )
    
    model_name = model.__class__.__name__

    # switch to train mode
    model.train()

    end = time.time()
    for i, batch in enumerate(train_loader):
        optimizer.zero_grad()
        step = epoch * len(train_loader) + i
        # measure data loading time
        data_time.update(time.time() - end)

        images = batch[0].to(device)
        target = batch[1].to(device)

        # compute output
        output = model(images)
        loss = criterion(output, target)

        # compute gradient
        loss.backward()
        optimizer.step()
        
        # measure accuracy and record loss
        acc_metric = accuracy(output, target)
        f1_metric = f1(output, target)
        precision_metric = precision(output, target)
        recall_metric = recall(output, target)
        
        losse_meter.update(loss.item(), n=images.size(0))
        accuracy_meter.update(acc_metric, n=images.size(0))
        f1_meter.update(f1_metric, n=images.size(0))
        precision_meter.update(precision_metric, n=images.size(0))
        recall_meter.update(recall_metric, n=images.size(0))
        
        writer.add_scalar(f'{model_name}-train-loss/{criterion.__class__.__name__}', loss.item(), step)
        writer.add_scalar(f'{model_name}-train-metric/accuracy', acc_metric, step)
        writer.add_scalar(f'{model_name}-train-metric/f1', f1_metric, step)
        writer.add_scalar(f'{model_name}-train-metric/precision', precision_metric, step)
        writer.add_scalar(f'{model_name}-train-metric/recall', recall_metric, step)
        
        writer.add_scalar(f'{model_name}-lr', optimizer.param_groups[0]['lr'], step)

        # measure elapsed time
        batch_time.update(time.time() - end)
        end = time.time()

        if i % print_freq == 0:
            progress.display(i)
    return {
        'loss_avg': losse_meter.avg, 'acc_avg': accuracy_meter.avg,
        'f1_avg': f1_meter.avg, 'precision_avg': precision_meter.avg,
        'recall_avg': recall_meter.avg
    }


def validate_disc_one_epoch(val_loader, model, criterion, epoch, device, print_freq, writer):
    batch_time = AverageMeter('Time', ':6.3f')
    losse_meter = AverageMeter('Loss', ':.4e')
    accuracy_meter = AverageMeter('Acc', ':6.2f')
    f1_meter = AverageMeter('F1', ':6.2f')
    precision_meter = AverageMeter('PR', ':6.2f')
    recall_meter = AverageMeter('RC', ':6.2f')
    progress = ProgressMeter(
        len(val_loader),
        [batch_time, losse_meter, accuracy_meter, f1_meter],
        prefix=f'Val Epoch: [{epoch}]'
    )
    
    model_name = model.__class__.__name__

    # switch to evaluate mode
    model.eval()

    with torch.no_grad():
        end = time.time()
        for i, batch in enumerate(val_loader):
            step = epoch * len(val_loader) + i
            
            images = batch[0].to(device)
            target = batch[1].to(device)

            # compute output
            output = model(images)
            loss = criterion(output, target)
            
            # measure accuracy and record loss
            acc_metric = accuracy(output, target)
            f1_metric = f1(output, target)
            precision_metric = precision(output, target)
            recall_metric = recall(output, target)
            
            losse_meter.update(loss.item(), n=images.size(0))
            accuracy_meter.update(acc_metric, n=images.size(0))
            f1_meter.update(f1_metric, n=images.size(0))
            precision_meter.update(precision_metric, n=images.size(0))
            recall_meter.update(recall_metric, n=images.size(0))
            
            writer.add_scalar(f'{model_name}-val-loss/{criterion.__class__.__name__}', loss.item(), step)
            writer.add_scalar(f'{model_name}-val-metric/accuracy', acc_metric, step)
            writer.add_scalar(f'{model_name}-val-metric/f1', f1_metric, step)
            writer.add_scalar(f'{model_name}-val-metric/precision', precision_metric, step)
            writer.add_scalar(f'{model_name}-val-metric/recall', recall_metric, step)

            # measure elapsed time
            batch_time.update(time.time() - end)
            end = time.time()

            if i % print_freq == 0:
                progress.display(i)

    return {
        'loss_avg': losse_meter.avg, 'acc_avg': accuracy_meter.avg,
        'f1_avg': f1_meter.avg, 'precision_avg': precision_meter.avg,
        'recall_avg': recall_meter.avg
    }
    
    
def train_autoencoder_model(model, optimizer, scheduler, criterion, train_dataloader, val_dataloader, opt, target_metric='f1_avg', best_target_metric=-np.inf):
    model_writer_path = opt.path_to_tensorboard_logs / model.__class__.__name__

    if model_writer_path.exists():
        shutil.rmtree(model_writer_path)
    writer = SummaryWriter(log_dir=str(model_writer_path))

    for epoch in range(opt.start_epoch, opt.epochs):
        # train for one epoch
        _ = train_autoencoder_one_epoch(train_dataloader, model, criterion, optimizer, epoch, opt.device, opt.print_freq, writer)

        # evaluate on validation set
        val_metrics = validate_autoencoder_one_epoch(val_dataloader, model, criterion, epoch, opt.device, opt.print_freq, writer)
        
        # learning rate scheduler step
        scheduler.step(val_metrics['loss_avg'])

        # remember best value and save checkpoint
        target_metric_value = val_metrics[target_metric]
        is_best = target_metric_value < best_target_metric
        best_target_metric = max(target_metric_value, best_target_metric)

        save_checkpoint(
            {
                'epoch': epoch,
                'state_dict': model.state_dict(),
                f'best_{target_metric}': best_target_metric,
                'optimizer' : optimizer.state_dict(),
            },
            is_best,
            filename=str(opt.path_to_models / f'{model.__class__.__name__}_checkpoint.pth'),
            best_filename=str(opt.path_to_models / f'{model.__class__.__name__}_model_best.pth'),
        )
    writer.close()


def train_autoencoder_one_epoch(train_loader, model, criterion, optimizer, epoch, device, print_freq, writer):
    batch_time = AverageMeter('Time', ':6.3f')
    data_time = AverageMeter('Data', ':6.3f')
    losse_meter = AverageMeter('Loss', ':.4e')
    progress = ProgressMeter(
        len(train_loader),
        [batch_time, data_time, losse_meter],
        prefix=f"Train Epoch: [{epoch}]"
    )
    
    model_name = model.__class__.__name__

    # switch to train mode
    model.train()

    end = time.time()
    for i, batch in enumerate(train_loader):
        optimizer.zero_grad()
        step = epoch * len(train_loader) + i
        # measure data loading time
        data_time.update(time.time() - end)

        images = add_gaussian_noise(batch[0]).to(device)
        target = batch[0].to(device)

        # compute output
        output = model(images)
        loss = criterion(output, target)

        # compute gradient
        loss.backward()
        optimizer.step()
        
        losse_meter.update(loss.item(), n=images.size(0))
        
        writer.add_scalar(f'{model_name}-train-loss/{criterion.__class__.__name__}', loss.item(), step)
        
        writer.add_scalar(f'{model_name}-lr', optimizer.param_groups[0]['lr'], step)

        # measure elapsed time
        batch_time.update(time.time() - end)
        end = time.time()

        if i % print_freq == 0:
            progress.display(i)
    
    return {
        'loss_avg': losse_meter.avg,
    }


def validate_autoencoder_one_epoch(val_loader, model, criterion, epoch, device, print_freq, writer):
    batch_time = AverageMeter('Time', ':6.3f')
    losse_meter = AverageMeter('Loss', ':.4e')
    progress = ProgressMeter(
        len(val_loader),
        [batch_time, losse_meter],
        prefix=f'Val Epoch: [{epoch}]'
    )
    
    model_name = model.__class__.__name__

    # switch to evaluate mode
    model.eval()

    with torch.no_grad():
        end = time.time()
        for i, batch in enumerate(val_loader):
            step = epoch * len(val_loader) + i
            
            images = add_gaussian_noise(batch[0]).to(device)
            target = batch[0].to(device)

            # compute output
            output = model(images)
            loss = criterion(output, target)
            
            losse_meter.update(loss.item(), n=images.size(0))
            
            writer.add_scalar(f'{model_name}-val-loss/{criterion.__class__.__name__}', loss.item(), step)

            # measure elapsed time
            batch_time.update(time.time() - end)
            end = time.time()

            if i % print_freq == 0:
                progress.display(i)
                
        grid = torch.cat([output[:20], target[:20]])
        grid = make_grid(grid, nrow=4, padding=0)
        writer.add_image(f'{model_name}-val-images/{criterion.__class__.__name__}', grid, step)

    return {
        'loss_avg': losse_meter.avg,
    }


def get_val_metrics(val_loader, model, device, add_noise=False):
    predictions = []
    targets = []
    
    # switch to evaluate mode
    model.eval()
    with torch.no_grad():
        for _, batch in tqdm(enumerate(val_loader), total=len(val_loader), desc='batch loop'):
            images = add_gaussian_noise(batch[0]).to(device) if add_noise else batch[0].to(device)
            target = batch[1].to(device)

            # compute output
            output = model(images)
            
            predictions.extend(torch.argmax(output, dim=1).detach().cpu().numpy())
            targets.extend(torch.argmax(target, dim=1).detach().cpu().numpy())
            
    acc_metric = accuracy_score(targets, predictions)
    f1_metric = f1_score(targets, predictions, average='weighted')
    precision_metric = precision_score(targets, predictions, average='weighted')
    recall_metric = recall_score(targets, predictions, average='weighted')
    
    conf_matrix = confusion_matrix(targets, predictions)
    
    return acc_metric, f1_metric, precision_metric, recall_metric, conf_matrix


def infer_disc_one_image(image, model, device, transform=None,):
    image = prepare_data_for_disc_model(image, transform,)
    model.eval()
    with torch.no_grad():
        image = image.to(device)
        output = model(image)
        predicted_class = torch.argmax(output, dim=1).detach().cpu().numpy()[0]
    
    return predicted_class


def infer_autoencoder_one_image(image, model, device, transform=None,):
    image = prepare_data_for_autoencoder_model(image, transform,)
    model.eval()
    with torch.no_grad():
        image = image.to(device)
        output = model(image).detach().cpu()
    
    return output
