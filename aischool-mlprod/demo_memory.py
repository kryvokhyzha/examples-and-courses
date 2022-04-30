import GPUtil
import torch
import torchvision


def get_device():
    return f"cuda:{torch.cuda.current_device()}" if torch.cuda.is_available() else "cpu"


def measure(use_half=True, batch_size=4):
    print("Init Model")
    device = get_device()
    dtype = torch.half if use_half else torch.float32
    model = torchvision.models.resnet50(pretrained=True, progress=True)
    torch.tensor([0]).to(device)
    print('Memory Used after zero tensor', GPUtil.getGPUs()[0].memoryUsed)

    model = model.eval().requires_grad_(False).to(dtype).to(device)
    torch.cuda.synchronize(device)
    print('Memory Used after model loaded in memory', GPUtil.getGPUs()[0].memoryUsed)

    frames = torch.randn(batch_size, 3, 512, 512).to(dtype)
    model(frames.to(device))
    print(f'Memory Used after model inference, batch_size {batch_size}', GPUtil.getGPUs()[0].memoryUsed)


def main():
    measure(use_half=False, batch_size=4)


if __name__ == "__main__":
    main()
