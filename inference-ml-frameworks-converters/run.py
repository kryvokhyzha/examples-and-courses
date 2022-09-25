import torch
import onnx
import os
import onnxruntime as ort
import tensorflow as tf
import coremltools as ct
import pandas as pd
import numpy as np
import click

from collections import defaultdict
from tqdm import tqdm
from onnx_tf.backend import prepare
from torch.utils.mobile_optimizer import optimize_for_mobile
from torchvision import transforms
from PIL import Image
from coremltools.models.neural_network.quantization_utils import quantize_weights

# converters
def torch_to_torchscript(model, sample_input, torchscript_model_path='models/model.pt',):
    os.makedirs(os.path.dirname(torchscript_model_path), exist_ok=True)

    traced_script_model = torch.jit.trace(model, sample_input)
    torch.jit.save(traced_script_model, torchscript_model_path)
    return traced_script_model


def torchscript_to_torchmobile_model(torchscript_model_path='models/model.pt', torchscript_mobile_model_path='models/mobile_model.pt'):
    os.makedirs(os.path.dirname(torchscript_model_path), exist_ok=True)

    torchscript_model = torch.jit.load(torchscript_model_path)
    # doesn't work with latest torch: https://discuss.pytorch.org/t/torch-utils-mobile-optimizer-optimize-for-mobile-is-resulting-different-output-than-torch-model-and-jit-model/150183/8
    # torchscript_model_optimized = optimize_for_mobile(traced_script_module)
    torchscript_model._save_for_lite_interpreter(torchscript_mobile_model_path)


def torchscript_to_coreml(labels, sample_input, torchscript_model_path='models/model.pt', coreml_model_path='models/model.mlmodel'):
    # normalization overview: https://coremltools.readme.io/docs/image-inputs#preprocessing-for-torch
    torchscript_model = torch.jit.load(torchscript_model_path)
    scale = 1/(0.226*255.0)
    bias = [-0.485/(0.229), -0.456/(0.224), -0.406/(0.225)]

    model = ct.convert(
        torchscript_model,
        inputs=[ct.ImageType(
            name="image",
            shape=ct.Shape(shape=sample_input.shape),
            scale=scale,
            bias=bias)],
        classifier_config=ct.ClassifierConfig(labels)
    )

    if isinstance(model, ct.models.model.MLModel):
        # When the export is done on MaxOS, return type is mlmodel
        spec = model.get_spec()
    else:
        # When the export is done on Linux, the return is spec
        spec = model

    ct.utils.rename_feature(spec, spec.description.output[0].name, 'classLabelProbs')
    ct.utils.save_spec(spec, coreml_model_path)
    try:
        # model can be used for inference only on MacOS
        return ct.models.MLModel(coreml_model_path)
    except Exception as ex:
        print(ex)
        return None


def torch_to_onnx(sample_input, torchscript_model_path='models/model.pt', onnx_model_path='models/model.onnx'):
    os.makedirs(os.path.dirname(torchscript_model_path), exist_ok=True)

    model = torch.jit.load(torchscript_model_path)
    torch.onnx.export(
        model,
        sample_input,
        onnx_model_path,
        verbose=False,
        input_names=['input'],
        output_names=['output'],
        opset_version=12,
        example_outputs=model(sample_input)
    )
    onnx_model = onnx.load(onnx_model_path)
    onnx.checker.check_model(onnx_model)
    ort_sess = ort.InferenceSession(onnx_model_path)
    return ort_sess


def onnx_to_tf(onnx_model_path='models/model.onnx', tf_model_path='models/model_tf'):
    os.makedirs(os.path.dirname(onnx_model_path), exist_ok=True)

    onnx_model = onnx.load(onnx_model_path)
    tf_rep = prepare(onnx_model)
    tf_rep.export_graph(tf_model_path)
    return tf_model_path


def tf_to_tflite(tf_model_path='models/model_tf', tflite_model_path='models/model.tflite'):
    os.makedirs(os.path.dirname(tf_model_path), exist_ok=True)

    converter = tf.lite.TFLiteConverter.from_saved_model(tf_model_path)
    tflite_model = converter.convert()
    with open(tflite_model_path, 'wb') as f:
        f.write(tflite_model)
    return tf.lite.Interpreter(tflite_model_path)

# inference
def torch_inference(model, features):
    with torch.no_grad():
        return model(features).data.numpy()


def onnx_inference(model, features):
    return model.run(None, {'input': features})[0]


def tflite_inference(interpreter, features):
    my_signature = interpreter.get_signature_runner()
    output = my_signature(input=tf.constant(features, shape=features.shape, dtype=tf.float32))
    return output['output']


def coreml_out_dict_to_list(coreml_dict, labels):
    out = []
    for x in labels:
        if x in coreml_dict:
            out.append(coreml_dict[x])
        else:
            out.append(None)
    return np.expand_dims(out, 0)


@click.command()
@click.option("--mode", type=click.Choice(['NCHW', 'NHWC']), default='NCHW')
@click.option("--softmax", type=bool, default=True)
def main(mode: str, softmax: bool):
    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]
    height, width = 224, 224

    preprocess = transforms.Compose([
        transforms.Resize(size=(height, width)),
        transforms.ToTensor(),
        transforms.Normalize(mean=mean, std=std)
    ])

    shape = (1, 3, height, width) if mode == 'NCHW' else (1, height, width, 3)
    labels = list(pd.read_csv('labels.csv', header=None)[0])
    sample_input = torch.rand(shape)

    base_model = torch.hub.load('pytorch/vision:v0.10.0', 'mobilenet_v2', pretrained=True).eval()

    class AdjustedModel(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.model = base_model

        def forward(self, x):
            if mode == 'NHWC':
                x = x.permute(0, 3, 1, 2)
            logits = self.model(x)
            if softmax:
                return torch.nn.functional.softmax(logits, dim=1)
            return logits

    model = AdjustedModel()
    torchscript_model = torch_to_torchscript(model, sample_input)
    if mode == 'NCHW':
        coreml_model = torchscript_to_coreml(labels, sample_input)
    else:
        coreml_model = None
    torchscript_to_torchmobile_model()
    onnx_model = torch_to_onnx(sample_input)
    _ = onnx_to_tf()
    tflite_model = tf_to_tflite()

    # verification test
    image = Image.open('images/image.jpeg')
    sample_input = preprocess(image).unsqueeze(0)
    if mode == 'NHWC':
        sample_input = sample_input.permute(0, 2, 3, 1)

    torch_out = torch_inference(model, sample_input)[0]
    torchscript_out = torch_inference(torchscript_model, sample_input)[0]
    onnx_out = onnx_inference(onnx_model, sample_input.data.numpy())[0]
    tflite_out = tflite_inference(tflite_model, sample_input.data.numpy())[0]
    if coreml_model:
        coreml_out = coreml_model.predict({'image': image.resize((height, width))})['classLabelProbs']
        coreml_out = coreml_out_dict_to_list(coreml_out, labels)[0]

    print(f'torch: {sorted(zip(labels, torch_out), key=lambda x: -x[1])[:3]}')
    print(f'torchscript: {sorted(zip(labels, torchscript_out), key=lambda x: -x[1])[:3]}')
    print(f'onnx: {sorted(zip(labels, onnx_out), key=lambda x: -x[1])[:3]}')
    print(f'tflite: {sorted(zip(labels, tflite_out), key=lambda x: -x[1])[:3]}')
    if coreml_model:
        print(f'coreml: {sorted(zip(labels, coreml_out), key=lambda x: -x[1])[:3]}')

    # define containers for quality conversion metrics here
    for _ in tqdm(range(100)):
        random_noise = torch.rand(shape)[0]
        random_image = transforms.ToPILImage()(random_noise)
        random_tensor = preprocess(random_image).unsqueeze(0)

        torch_out = torch_inference(model, random_tensor)
        torchscript_out = torch_inference(torchscript_model, random_tensor)
        onnx_out = onnx_inference(onnx_model, random_tensor.data.numpy())
        tflite_out = tflite_inference(tflite_model, random_tensor.data.numpy())
        if coreml_model:
            coreml_out = coreml_model.predict({'image': random_image})['classLabelProbs']
            coreml_out = coreml_out_dict_to_list(coreml_out, labels)

        assert torch_out.shape == torchscript_out.shape == onnx_out.shape == tflite_out.shape == coreml_out.shape == (1, 1000)

        # measure and store conversion quality metrics for a given sample here

    # print/plot final metrics here

if __name__ == '__main__':
    main()
