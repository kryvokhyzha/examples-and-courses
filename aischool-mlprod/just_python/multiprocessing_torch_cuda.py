import os

os.environ['MKL_NUM_THREADS'] = "1"
os.environ['OMP_NUM_THREADS'] = "1"

import time
from threading import Thread
from PIL import Image
import numpy as np
import torch
torch.set_num_threads(1)

import torchvision
from multiprocessing import Pool, Process
import SharedArray as sa

model = torchvision.models.mobilenet_v3_large(pretrained=True, progress=True)
# change for cuda
device = 'cuda:0'
CORES = 2
# import multiprocessing as mp
# mp.set_start_method('spawn')
#
model = model.eval().requires_grad_(False).to(torch.float32).to(device)


def resize(image, shape):
    return np.array(Image.fromarray(image).resize(shape))


def processing(im_frames):
    print('processing', im_frames.shape)
    resized = [resize(frame, (256, 256)) for frame in im_frames]
    results = [model(torch.tensor(frame).permute(2, 0, 1).div(255).unsqueeze(0).to(device)) for frame in resized]
    [resize(frame, (3840, 2160)) for frame in resized]
    max_ = [x.cpu().numpy().argmax() for x in results]
    print('mean result value',np.array(max_).mean())
    return max_


def run_single_thread(frames):
    start = time.time()
    processing(frames)
    end = time.time()
    print('Elapsed time single thread:', end - start)


def run_multi_thread(frames, cores=CORES):
    start = time.time()
    n = len(frames) // cores
    threads = [Thread(target=processing, args=(frames[n * i: n * (i + 1)],)) for i in range(cores)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    end = time.time()
    print(f'Elapsed time {cores} threads:', end-start)


def run_multi_process(frames, cores=CORES):
    pool = Pool(processes=cores)
    n = len(frames) // cores
    start = time.time()
    [pool.map_async(processing, (frames[n * i: n * (i + 1)],)) for i in range(cores)]
    pool.close()
    pool.join()
    end = time.time()
    print(f'Elapsed time {cores} processes:', end-start)


def processing_shm(shm_name, shape, start_index, end_index):
    loaded_slice = sa.attach(shm_name)[start_index:end_index]
    processing(loaded_slice)


def make_shared_np_array(frames):
    name = "shm://test6"
    shm = sa.create(name, frames.shape, dtype=np.uint8)
    shm[:] = frames[:]
    return name


def run_multi_process_shm(frames, cores=CORES):
    pool = Pool(processes=cores)
    shm_name = make_shared_np_array(frames)
    n = len(frames) // cores
    start = time.time()
    [pool.apply_async(processing_shm, args=(shm_name, frames.shape, n * i, n * (i + 1),)) for i in range(cores)]
    pool.close()
    pool.join()
    end = time.time()
    print(f'Elapsed time {cores} shm processes:', end-start)
    sa.delete(shm_name)


def run_multi_process_shm_no_pool(frames, cores=CORES):
    shm_name = make_shared_np_array(frames)
    n = len(frames) // cores
    processes = [Process(target=processing_shm, args=(shm_name, frames.shape, n * i, n * (i + 1),)) for i in range(cores)]
    start = time.time()
    [p.start() for p in processes]
    [p.join() for p in processes]
    end = time.time()
    print(f'Elapsed time {cores} shm processes (no pool):', end-start)
    sa.delete(shm_name)


if __name__ == '__main__':
    frames = np.random.randint(255, size=(32, 3840, 2160, 3), dtype=np.uint8)
    run_single_thread(frames)
    time.sleep(2)
    run_multi_thread(frames)
    time.sleep(2)
    run_multi_process(frames)
    time.sleep(2)
    run_multi_process_shm(frames)
    time.sleep(2)
    # run_multi_process_shm_no_pool(frames)
