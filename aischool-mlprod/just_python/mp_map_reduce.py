import time

import numpy as np
from multiprocessing import Process, Queue
import SharedArray as sa
import torchvision
import torch
torch.set_num_threads(1)
from PIL import Image

CORES = 16
shm_name = "shm://test7"
device = 'cpu'


def make_shared_np_array(frames):
    name = shm_name
    shm = sa.create(name, frames.shape, dtype=np.uint8)
    shm[:] = frames[:]
    return name


def resize(image, shape):
    return np.array(Image.fromarray(image).resize(shape))


def processing(model, im_frames):
    print('processing', im_frames.shape)
    resized = [resize(frame, (256, 256)) for frame in im_frames]
    results = [model(torch.tensor(frame).permute(2, 0, 1).div(255).unsqueeze(0).to(device)) for frame in resized]
    [resize(frame, (3840, 2160)) for frame in resized]
    max_ = [x.cpu().numpy().argmax() for x in results]
    print('mean result value',np.array(max_).mean())
    return max_


def run_creator(process_queue):
    time.sleep(10)
    frames = np.random.randint(255, size=(32, 3840, 2160, 3), dtype=np.uint8)
    shm_name = make_shared_np_array(frames)
    n = len(frames) // CORES
    print('num_batches', CORES, 'frames_in_batch', n)
    start = time.time()
    [process_queue.put((shm_name, frames.shape, start, CORES, n * i, n * (i + 1))) for i in range(CORES)]


def run_cleaner(clean_queue):
    counter = 0
    while True:
        item = clean_queue.get()
        if item is not None:
            name, start, num_frames = item
            counter += 1
            if counter == num_frames:
                end = time.time()
                print(counter, num_frames)
                sa.delete(shm_name)
                print(f'Elapsed time:', end - start)
        else:
            time.sleep(0.01)


def run_processing(process_queue, cleaner_queue):
    model = torchvision.models.mobilenet_v3_large(pretrained=True, progress=True)
    model = model.eval().requires_grad_(False).to(torch.float32).to(device)

    while True:
        item = process_queue.get()
        if item is not None:
            shm_name, shape, start, num_items, st_idx, end_idx = item
            loaded_slice = sa.attach(shm_name)[st_idx:end_idx]
            processing(model, loaded_slice)
            cleaner_queue.put((shm_name, start, num_items))
        else:
            time.sleep(0.01)


def main():
    queue = Queue()
    cleaner_queue = Queue()
    creator = Process(target=run_creator, args=(queue,))
    processor1 = Process(target=run_processing, args=(queue, cleaner_queue))
    processor2 = Process(target=run_processing, args=(queue, cleaner_queue))
    processor3 = Process(target=run_processing, args=(queue, cleaner_queue))
    processor4 = Process(target=run_processing, args=(queue, cleaner_queue))
    processor5 = Process(target=run_processing, args=(queue, cleaner_queue))
    processor6 = Process(target=run_processing, args=(queue, cleaner_queue))
    processor7 = Process(target=run_processing, args=(queue, cleaner_queue))
    processor8 = Process(target=run_processing, args=(queue, cleaner_queue))
    processor9 = Process(target=run_processing, args=(queue, cleaner_queue))
    processor10 = Process(target=run_processing, args=(queue, cleaner_queue))
    processor11 = Process(target=run_processing, args=(queue, cleaner_queue))
    processor12 = Process(target=run_processing, args=(queue, cleaner_queue))
    processor13 = Process(target=run_processing, args=(queue, cleaner_queue))
    processor14 = Process(target=run_processing, args=(queue, cleaner_queue))
    processor15 = Process(target=run_processing, args=(queue, cleaner_queue))
    processor16 = Process(target=run_processing, args=(queue, cleaner_queue))
    cleaner = Process(target=run_cleaner, args=(cleaner_queue,))
    processes = [creator, processor1, processor2, processor3, processor4, processor5, processor6, processor7, processor8, processor9, processor10, processor11, processor12, processor13, processor14, processor15, processor16, cleaner]

    [p.start() for p in processes]
    [p.join() for p in processes]


if __name__ == '__main__':
    main()
