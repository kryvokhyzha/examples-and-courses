import time
from PIL import Image
import numpy as np
import torch
torch.set_num_threads(1)
from threading import Thread
from multiprocessing import Pool, Process

import torchvision

CORES = 8
device = 'cpu'
model = torchvision.models.mobilenet_v3_large(pretrained=True, progress=True)
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
    print(f'Elapsed time {cores} cores threads:', end-start)


def run_multi_process(frames, cores=CORES):
    start = time.time()
    n = len(frames) // cores
    threads = [Process(target=processing, args=(frames[n * i: n * (i + 1)],)) for i in range(cores)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    end = time.time()
    print(f'Elapsed time {cores} cores processes:', end-start)


# def run_multi_process(frames, cores=CORES):
#     pool = Pool(processes=cores)
#     n = len(frames) // cores
#     start = time.time()
#     [pool.map_async(processing, (frames[n * i: n * (i + 1)],)) for i in range(cores)]
#     pool.close()
#     pool.join()
#     end = time.time()
#     print(f'Elapsed time {cores} processes:', end-start)


if __name__ == '__main__':
    frames = np.random.randint(255, size=(32, 3840, 2160, 3), dtype=np.uint8)
    # run_single_thread(frames)
    run_multi_thread(frames)
    run_multi_process(frames)
