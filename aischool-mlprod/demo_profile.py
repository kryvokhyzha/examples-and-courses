'''
For more details look here:
https://pytorch.org/tutorials/recipes/recipes/profiler_recipe.html
'''

import torch
import torchvision
from torch.profiler import profile, record_function, ProfilerActivity


def get_device():
    return f"cuda:{torch.cuda.current_device()}" if torch.cuda.is_available() else "cpu"


def measure(use_half=True, batch_size=4, device='cpu'):
    print("Init Model")
    dtype = torch.half if use_half else torch.float32
    model = torchvision.models.resnet50(pretrained=True, progress=True)
    model = model.eval().requires_grad_(False).to(dtype).to(device)

    frames = torch.randn(batch_size, 3, 128, 128).to(dtype).to(device)
    activity = ProfilerActivity.CPU if device =='cpu' else ProfilerActivity.CUDA
    with profile(activities=[activity], record_shapes=True, profile_memory=True) as prof:
        with record_function("model_inference"):
            model(frames)
    '''
    Valid keys include: ``cpu_time``, ``cuda_time``, ``cpu_time_total``,
                ``cuda_time_total``, ``cpu_memory_usage``, ``cuda_memory_usage``,
                ``self_cpu_memory_usage``, ``self_cuda_memory_usage``, ``count``.
    '''
    dvc = 'cpu' if device == 'cpu' else 'cuda'
    print(prof.key_averages(group_by_input_shape=True).table(sort_by=f"{dvc}_time_total", row_limit=10))
    print(prof.key_averages(group_by_input_shape=True).table(sort_by=f"self_{dvc}_memory_usage", row_limit=10))


def main():
    measure(use_half=False, batch_size=4, device='cpu')
    print("************")
    # measure(use_half=False, batch_size=4, device='cuda:0')


if __name__ == "__main__":
    main()
