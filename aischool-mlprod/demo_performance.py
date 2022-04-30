import time

import GPUtil
import numpy as np
import torch
import torchvision


def get_device():
    return f"cuda:{torch.cuda.current_device()}" if torch.cuda.is_available() else "cpu"


def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


def measure(iterations=10, init_iterations=2, batch_size=4, use_jit=True, use_half=True):
    print("Init Model")
    device = get_device()
    dtype = torch.half if use_half else torch.float32
    model = torchvision.models.mobilenet_v3_small(pretrained=True, progress=True)
    memory_before_init = GPUtil.getGPUs()[0].memoryUsed
    image_size = 512

    model = model.eval().requires_grad_(False).to(dtype).to(device)
    if use_jit:
        mock_tensor = torch.randn((batch_size, 3, image_size, image_size)).to(dtype).to(device)
        model = torch.jit.trace(model, mock_tensor)

    memory_after_init = GPUtil.getGPUs()[0].memoryUsed
    torch.cuda.synchronize(device)

    frames = torch.randn((batch_size * iterations, 3, image_size, image_size)).to(dtype)
    print("Test with data")

    times = []
    for i in range(iterations):
        print(f"Iteration: {i}")
        for batch_index, frames_batch in enumerate(batch(frames, n=batch_size)):
            time1 = time.time()
            cuda_batch = frames_batch.to(device)   # try moving it's from time measurement - difference ~3%
            _ = model(cuda_batch).cpu()
            torch.cuda.synchronize(device)
            time2 = time.time()
            iter_time = time2 - time1
            times.append([iter_time])

    memory_after = GPUtil.getGPUs()[0].memoryUsed
    total_iterations = len(times)
    print(f"Total batches: {total_iterations}")
    print(f"Batch Size: {batch_size} | Use Half: {use_half} | Use JIT: {use_jit} | "
          f"GPU Mem Init Usage: {memory_after_init - memory_before_init} | GPU Mem NN usage: {memory_after - memory_after_init}")
    print(f"Total speed: {1 / (np.sum(times[init_iterations:]) / (total_iterations - init_iterations) / batch_size)} FPS")


def main():
    measure(use_half=False, use_jit=False, batch_size=1)


if __name__ == "__main__":
    main()
