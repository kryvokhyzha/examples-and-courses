import base64
import io
import os

import numpy as np
from PIL import Image
import sys

from imageio import imread, imsave
import cv2

sys.path.append('models')

from models.face_parser_handler import FaceParserHandler


def make_context(ts_path, model_dir='./', gpu_id='0'):
    context = type('', (), {})()
    context.system_properties = {'model_dir': f'{model_dir}', 'gpu_id': gpu_id}
    context.manifest = {'model': {'serializedFile': f'{ts_path}'}}
    return context


class Demo:
    def __init__(self):
        self.fp_handler = FaceParserHandler()
        self.fp_handler.initialize(make_context('weights/faceparser_bisenet.ts', f'models'))

    def run_face_parser(self, image):
        return self.fp_handler([{'image': image}])[0]


if __name__ == '__main__':
    os.makedirs('output', exist_ok=True)
    runner = Demo()
    image = imread('../data/musk.jpg')
    image = cv2.resize(image, (512, 512))

    result = runner.run_face_parser(image)
    head = result['head']
    head_img = np.array(Image.open(io.BytesIO(base64.b64decode(head))))
    imsave('output/musk_head_torchserve.png', head_img)

    print('ok')
