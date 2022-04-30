import logging
from http import HTTPStatus
from typing import List

import bentoml
import numpy as np
import cv2
from bentoml.types import InferenceError, InferenceResult
from face_parser import FaceParser

from parser_service import config
from parser_service.validators import InferenceData
from parser_service.adapters import ImageDataInput


class FaceParserService(bentoml.BentoService):
    def __init__(self, serving=True):
        super(FaceParserService, self).__init__()
        if serving:
            self.face_parser = FaceParser(
                device=config.device,
                use_half=config.half_precision,
            )

    @bentoml.api(input=ImageDataInput(), batch=True)
    def predict(self, tasks_list: List[InferenceData]) -> List[InferenceResult]:
        results = []
        try:
            images = [cv2.resize(task.image[:, :, :3], (config.image_size, config.image_size)) for task in tasks_list]
            head_results = self.face_parser.predict(np.array(images))
            results.extend(InferenceResult(data=r.tobytes(), http_status=HTTPStatus.OK) for r in head_results)
        except Exception as exc:
            err_msg = f"Errors during prediction {exc}"
            logging.exception(err_msg, extra={"request_id": "request_id"})  # Add request id and other helpful info to the extra
            results.append([InferenceError(err_msg=err_msg)] * len(tasks_list))
        return results
