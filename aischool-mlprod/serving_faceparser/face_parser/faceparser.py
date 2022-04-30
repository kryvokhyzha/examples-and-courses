import pkg_resources
import torch
import cv2
import numpy as np

from .models.bisenet import BiSeNet
from torchvision.transforms import Normalize


class FaceParser:
    weights_path = pkg_resources.resource_filename(__name__, 'weights/bisenet.pth')

    def __init__(self, device='cuda:0', use_half=True):
        self.device = device
        self.dtype = torch.half if use_half else torch.float
        self.model = BiSeNet(n_classes=19)
        self.model.load_state_dict(torch.load(self.weights_path, map_location=self.device))
        self.model = self.model.eval().to(self.device, dtype=self.dtype)

    @staticmethod
    def _compose_with_mask(image, mask, background=None, threshold_value=128):
        background = np.zeros_like(image) if background is None else background
        mask[mask < threshold_value] = 0
        composite = mask / 255 * image + (1 - mask / 255) * background
        return np.concatenate((composite.round().astype(np.uint8), mask), axis=2)

    def preprocess(self, images):
        image_tensor = torch.tensor(np.array(images)).to(self.device, dtype=self.dtype).permute(0, 3, 1, 2).div_(255)
        return Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))(image_tensor)

    def predict(self, images):
        with torch.no_grad():
            return self.postprocess(self.model(self.preprocess(images)), images)

    def postprocess(self, model_result, images, indexes_to_remove=(0, 14, 15, 16)):
        masks_batch = model_result[0].cpu().numpy()
        results_batch = []
        for item_index, mask in enumerate(masks_batch):
            for ind in indexes_to_remove:
                mask[ind] = np.zeros(mask[0].shape)
            head_mask = (np.amax(mask, axis=0) * 255/mask.max()).round().astype(np.uint8)
            _, mask_thresholded = cv2.threshold(head_mask, 128*1.2, 255, cv2.THRESH_BINARY)
            mask_filled = cv2.erode(cv2.dilate(mask_thresholded, np.ones((100, 100), 'uint8')), np.ones((100, 100), 'uint8'))
            head = self._compose_with_mask(images[item_index], mask_filled[..., None], threshold_value=128)
            results_batch.append(head)
        return results_batch
