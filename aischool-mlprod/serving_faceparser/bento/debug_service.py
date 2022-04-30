import os
import numpy as np
import requests
from imageio import imread, imsave

from parser_service.service import FaceParserService
from parser_service.validators import InferenceData


def debug_direct(crop1, crop2):
    face_swap_service = FaceParserService()
    #
    item1 = InferenceData(image=crop1)
    item2 = InferenceData(image=crop2)
    results = face_swap_service.predict([item1, item2])
    for index, result in enumerate(results):
        img = np.frombuffer(result.data, dtype="uint8").reshape(512, 512, 4)
        imsave(f'output/head_{index}.png', img)
    print('ok')


def debug_http(crop1):
    # python make_service.py && bentoml serve FaceParserService:latest
    file = {"image": (f'1.jpg', crop1.tobytes())}

    response = requests.post("http://0.0.0.0:5000/predict", files=file)
    result = np.frombuffer(response.content, dtype="uint8").reshape(512, 512, 4)
    imsave(f'output/head_bento_service.png', result)
    print('ok')


if __name__ == '__main__':
    os.makedirs('output', exist_ok=True)
    crop1 = imread('../data/musk.jpg').astype("uint8")
    crop2 = imread('data/emma_full.jpg').astype("uint8")
    #
    # debug_direct(crop1, crop2)
    debug_http(crop2)
    print('ok')
