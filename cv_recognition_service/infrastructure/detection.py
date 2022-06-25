import json
from typing import List

import numpy as np
import cv2

from infrastructure.interface import (
    DetectionModel,
    DetectionData,
)
from infrastructure.retina_torch.retina_api import RetinaDetector


class DummyDetector(DetectionModel):
    def __init__(self, model_path: str, conf_thresh: float) -> None:
        self.conf_thresh = conf_thresh
        self.model = self._load_model(model_path)

    def _load_model(self, model_path: str):
        def empty(image: np.ndarray):
            return [(274, 233, 300, 330, 0.98), (333, 201, 433, 320, 0.98)]

        return empty

    def _image_preprocessing(self, image: np.ndarray) -> np.ndarray:
        return cv2.resize(image, (600, 600))

    def detect(self, image: np.ndarray) -> List[DetectionData]:
        preprocessed_image = self._image_preprocessing(image)
        raw_predictions = self.model(preprocessed_image)
        predictions = self._raw_to_data(raw_predictions)
        return predictions

    def _raw_to_data(self, raw_predictions: list) -> List[DetectionData]:
        data_list = []
        for pred in raw_predictions:
            x_min = pred[0]
            y_min = pred[1]
            x_max = pred[2]
            y_max = pred[3]
            score = pred[4]
            class_name = "face"
            if score > self.conf_thresh:
                data_model = DetectionData(
                    x_min, y_min, x_max, y_max, score, face=None, class_name=class_name
                )
                data_list.append(data_model)
        return data_list


class RetinaTorchDetector(DetectionModel):
    def __init__(self, model_path: str, conf_thresh: float) -> None:
        self.conf_thresh = conf_thresh
        self._face_detector = self._load_model(model_path)

    def _load_model(self, model_path: str):
        with open(model_path, "r") as fin:
            retina_cfg = json.load(fin)
        face_detector = RetinaDetector(retina_cfg)
        return face_detector

    def _image_preprocessing(self, image: np.ndarray) -> np.ndarray:
        return cv2.resize(image, (840, 840))

    def detect(self, image: np.ndarray) -> List[DetectionData]:
        # preprocessed_image = self._image_preprocessing(image)
        raw_predictions = self._face_detector.get_faces(image)
        predictions = self._raw_to_data(raw_predictions)
        return predictions

    def _raw_to_data(self, raw_predictions: list) -> List[DetectionData]:
        coordinate_faces, faces = raw_predictions

        data_list = []
        for coord, face in zip(coordinate_faces, faces):
            x_min = coord[0]
            y_min = coord[1]
            x_max = coord[2]
            y_max = coord[3]
            score = coord[4]
            class_name = "face"
            if score > self.conf_thresh:
                data_model = DetectionData(
                    x_min, y_min, x_max, y_max, score, face, class_name
                )
                data_list.append(data_model)
        return data_list
