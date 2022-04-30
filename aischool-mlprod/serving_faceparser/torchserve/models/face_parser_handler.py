import logging
import os
import io
import cv2

import numpy as np
import torch
import base64
from PIL import Image
from torchvision.transforms import Normalize
from imageio import imsave
from ts.torch_handler.base_handler import BaseHandler

from face_parser import FaceParser

logger = logging.getLogger(__name__)


def save_image_bytes(np_img, format='PNG'):
    assert format in ['PNG', 'JPG']
    kwargs = {'quality': 80, 'optimize': True} if format =='JPG' else {}
    b = io.BytesIO()
    imsave(b, np_img, format=format, **kwargs)
    b.seek(0)
    return base64.b64encode(b.read()).decode('utf-8')


def decode_image(image):
    if isinstance(image, str):
        image = base64.b64decode(image)
    if isinstance(image, (bytearray, bytes)):
        image = np.array(Image.open(io.BytesIO(image)))
    return image


class FaceParserHandler(BaseHandler):
    def __init__(self):
        super(BaseHandler, self).__init__()
        self._context = None
        self.initialized = False
        self.model = None
        self.device = f"cuda:{torch.cuda.device_count() - 1}"
        self.face_parser = FaceParser(device=self.device, load_model=False)
        self.device = torch.device(self.device)

    def initialize(self, context):
        model_dir = context.system_properties.get('model_dir')
        serialized_file = context.manifest['model']['serializedFile']
        model_pt_path = os.path.join(model_dir, serialized_file)

        torch.set_grad_enabled(False)
        torch._C._jit_set_bailout_depth(1)
        self.model = torch.jit.load(model_pt_path, map_location=self.device)
        logger.debug(f'Model loaded from {model_dir}')
        self.model.eval()

        random_batch = torch.rand((1, 3, 512, 512)).half().to(self.device)
        self.model(random_batch)
        self.model(random_batch)
        self.initialized = True

    def __call__(self, items):
        return self.postprocess(self.inference(self.preprocess(items)))

    def preprocess(self, data):
        items = []
        for row in data:
            # if row.get('body'):
            #     row = pickle.loads(row.get('body'))
            image = row.get('image')
            image = decode_image(image)

            image_tensor = torch.tensor(np.array([image])).half().to(self.device).permute(0, 3, 1, 2).div_(255)
            preprocessed = Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))(image_tensor)
            items.append({'image': image, 'image_tensor': preprocessed})
        return items

    def inference(self, items, *args, **kwargs):
        with torch.no_grad():
            # currently no batching here
            for item in items:
                item['head_masks'] = self.model(item['image_tensor'].to(self.device))[0].cpu()[0]
            return items

    def postprocess(self, items):
        all_results = []

        for item in items:
            head = self._get_head(item['head_masks'], item['image'])
            all_results.append({'head': save_image_bytes(head)})
        return all_results

    def _get_head(self, model_result, image, indexes_to_remove=(0, 14, 15, 16)):
        mask = model_result.numpy()
        for ind in indexes_to_remove:
            mask[ind] = np.zeros(mask[0].shape)
        head_mask = (np.amax(mask, axis=0) * 255/mask.max()).round().astype(np.uint8)
        _, mask_thresholded = cv2.threshold(head_mask, 128*1.2, 255, cv2.THRESH_BINARY)
        mask_filled = cv2.erode(cv2.dilate(mask_thresholded, np.ones((100, 100), 'uint8')), np.ones((100, 100), 'uint8'))
        head = self._compose_with_mask(image, mask_filled[..., None], threshold_value=128)
        return head

    @staticmethod
    def _compose_with_mask(image, mask, background=None, threshold_value=128):
        background = np.zeros_like(image) if background is None else background
        mask[mask < threshold_value] = 0
        composite = mask / 255 * image + (1 - mask / 255) * background
        return np.concatenate((composite.round().astype(np.uint8), mask), axis=2)


