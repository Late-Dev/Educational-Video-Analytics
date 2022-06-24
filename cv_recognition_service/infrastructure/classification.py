import numpy as np
import cv2

from cv_recognition_service.infrastructure.interface import ClassificationModel, ClassificationData


class DummyClassifier(ClassificationModel):

    def __init__(self, model_path: str, conf_thresh: float) -> None:
        self.conf_thresh = conf_thresh
        self.model = self._load_model(model_path)

    def _load_model(self, model_path: str):
        def empty(image: np.ndarray):
            return ("happy", "0", 0.98)
        return empty
    
    def _image_preprocessing(self, image: np.ndarray) -> np.ndarray:
        return cv2.resize(image, (224, 224))


    def detector(self, image: np.ndarray):
        preprocessed_image = self._image_preprocessing(image)
        raw_predictions = self.model(preprocessed_image)
        predictions = ClassificationData(raw_predictions[0], raw_predictions[1], raw_predictions[2])
        return predictions
        