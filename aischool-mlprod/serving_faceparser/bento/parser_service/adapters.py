import base64
import io
import logging

from http import HTTPStatus
from typing import List, Sequence, Tuple

from PIL import Image
import numpy as np
import pydantic
from bentoml.adapters import MultiFileInput
from bentoml.types import FileLike, InferenceTask

from .validators import InferenceData

MultiFileTask = InferenceTask[Tuple[FileLike, ...]]


class ImageDataInput(MultiFileInput):
    """This input data adapter supports both image file and json on input and maps it to `InferenceData` type."""

    def __init__(self):
        super(ImageDataInput, self).__init__(input_names=["image"])

    def extract_user_func_args(self, tasks: Sequence[MultiFileTask]) -> Tuple[List[InferenceData]]:
        parsed_inputs = []
        for task in map(lambda t: t.data, tasks):
            try:
                image_array = np.frombuffer(task[0].stream.read(), dtype="uint8").reshape((512, 512, 3))
                result = InferenceData(image=image_array)
                parsed_inputs.append(result)
            except pydantic.ValidationError as exc:
                err_msg = f"Could not validate an input data {exc.errors()}"
                ImageDataInput._discard(task, err_msg, {"request_id": "request_id"})
            except AssertionError as exc:
                err_msg = f"Could not validate an input data {exc}"
                ImageDataInput._discard(task, err_msg, {"request_id": "request_id"})
        return (parsed_inputs,)

    @staticmethod
    def _discard(task, msg, extra):
        logging.error(msg, extra=extra)
        task.discard(http_status=HTTPStatus.BAD_REQUEST, err_msg=msg)
