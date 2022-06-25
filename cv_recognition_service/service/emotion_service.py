from typing import List
import numpy as np

from infrastructure.interface import DetectionModel
from infrastructure.interface import ClassificationModel
from infrastructure.tracking.wrapper import DeepsortTracker
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

    def process_frame(self, frame: np.ndarray) -> FrameData:
        detections_data = self.detection_model.detect(frame)

        cropped_images = self._crop_images(frame, detections_data)
        classes_data = [
            self.classification_model.predict(img) for img in cropped_images
        ]
        
        bboxes = [i.bbox for i in detections_data]
        scores = [i.score for i in detections_data]
        names = [i.class_name for i in detections_data]
        tracked_boxes = self.tracking_model.track_boxes(
            frame=frame,
            boxes=bboxes,
            scores=scores,
            names=names,
        )
        frame_data = self._serialize_frame_data(tracked_boxes, classes_data)
        plotted_frame = self._draw_predictions(frame, frame_data)
        return plotted_frame
