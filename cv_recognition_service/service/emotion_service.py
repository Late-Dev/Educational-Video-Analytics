from typing import List
import numpy as np

from infrastructure.interface import DetectionModel, DetectionData
from infrastructure.interface import ClassificationModel, ClassificationData
from service.interface import BaseService, FrameData


class DummyEmotionService(BaseService):
    def __init__(
        self,
        detection_model: DetectionModel,
        classification_model: ClassificationModel,
        det_threshold=0.9,
        cls_thresh=0.9,
    ):

        self.detection_model = detection_model
        self.classification_model = classification_model

    def process_frame(self, frame: np.ndarray) -> FrameData:
        detections_data = self.detection_model.detect(frame)

        cropped_images = self._crop_images(frame, detections_data)
        classes_data = [
            self.classification_model.predict(img) for img in cropped_images
        ]

        frame_data = self._serialize_frame_data(detections_data, classes_data)
        plotted_frame = self._draw_predictions(frame, frame_data)
        return plotted_frame
