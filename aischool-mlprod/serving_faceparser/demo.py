import os
import cv2
import torch
from imageio import imread, imsave
from face_parser import FaceParser


if __name__ == '__main__':
    os.makedirs('output', exist_ok=True)
    img_size = 512

    faceparser = FaceParser()

    image = imread('data/musk.jpg')
    image = cv2.resize(image, (512, 512))

    result = faceparser.predict([image])[0]
    imsave('output/musk_head.png', result)

    ##########
    ########## Let's trace model and check
    ##########

    image_example = torch.rand(1, 3, img_size, img_size).half()
    torch._C._jit_set_bailout_depth(1)
    torch.set_grad_enabled(False)
    traced_model = torch.jit.trace(faceparser.model, (image_example.to(faceparser.device)))

    ts_file_path = 'torchserve/models/weights/faceparser_bisenet.ts'
    torch.jit.save(traced_model, ts_file_path)
    ts_model_loaded = torch.jit.load(ts_file_path)

    image_tensor = faceparser.preprocess([image])
    result = ts_model_loaded(image_tensor)
    result_traced = faceparser.postprocess(result, [image])[0]

    imsave('output/musk_head_traced.png', result_traced)

    assert abs(result.mean() - result_traced.mean()) < 0.01
    print('ok')

