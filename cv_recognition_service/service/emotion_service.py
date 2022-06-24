from typing import List
import numpy as np

from cv_recognition_service.infrastructure.interface import DetectionModel
from cv_recognition_service.infrastructure.interface import ClassificationModel
from cv_recognition_service.infrastructure.tracking.wrapper import DeepsortTracker
from cv_recognition_service.service.interface import BaseService, FrameData


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

    def process_frame(self, frame: np.ndarray) -> List[FrameData]:
        detections_data = self.detection_model.detect(frame)
        cropped_images = self._crop_images()


class EmotionService(BaseService):
    def __init__(
        self,
        detection_model: DetectionModel,
        classification_model: ClassificationModel,
        tracking_model: DeepsortTracker,
        det_threshold=0.9,
        cls_thresh=0.9,
    ):
        self.detection_model = detection_model
        self.tracking_model = tracking_model
        self.classification_model = classification_model
        self.det_threshold = det_threshold
        self.cls_thresh = cls_thresh

    def process_frame(self, frame: np.ndarray) -> List[FrameData]:
        detections_data = self.detection_model.detect(frame)
        bboxes = [i.bbox for i in detections_data]
        scores = [i.score for i in detections_data]
        names = [i.class_name for i in detections_data]
        tracked_boxes = self.tracking_model.track_boxes(
            frame=frame,
            boxes=bboxes,
            scores=scores,
            names=names,
        )
        cropped_images = self._crop_images()
        # TODO Add postprocessing
