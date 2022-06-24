from typing import List
import numpy as np

from cv_recognition_service.infrastructure.interface import DetectionModel, DetectionData
from cv_recognition_service.infrastructure.interface import ClassificationModel, ClassificationData
from cv_recognition_service.service.interface import BaseService, FrameData


class DummyEmotionService(BaseService):

    def __init__(
        self, 
        detection_model: DetectionModel, 
        classification_model: ClassificationModel, 
        det_threshold=0.9, 
        cls_thresh=0.9):

        self.detection_model = detection_model
        self.classification_model = classification_model

    def process_frame(self, frame: np.ndarray) -> List[FrameData]:
        detections_data = self.detection_model.detect(frame)
        cropped_images = self._crop_images()
