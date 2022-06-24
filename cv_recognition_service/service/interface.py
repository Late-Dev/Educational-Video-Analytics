from abc import abstractmethod, ABC
from typing import List, Tuple
from dataclasses import dataclass

import numpy as np
import cv2

from infrastructure.interface import DetectionModel, DetectionData
from infrastructure.interface import ClassificationModel, ClassificationData


@dataclass
class FrameData:
    faces_detections: List[DetectionData]
    classes_data: List[ClassificationData]


class BaseService(ABC):

    @abstractmethod
    def __init__(self, detection_model: DetectionModel, classification_model: ClassificationModel) -> None:
        self.detection_model = detection_model
        self.classification_model = classification_model

    @abstractmethod
    def process_frame(self, frame: np.ndarray) -> List[FrameData]:
        pass

    @staticmethod
    def _crop_images(image: np.ndarray, det_predictions: List[DetectionData]):
        cropped_images = []
        for det_data in det_predictions:
            cropped = image[det_data.y_min:det_data.y_min+det_data.height, det_data.x_min:det_data.x_min+det_data.width]
            cropped_images.append(cropped)
        return cropped_images

    @staticmethod
    def _draw_predictions(frame: np.ndarray, frame_data: FrameData):
        fontScale = 1
        thickness = 3
        font = cv2.FONT_HERSHEY_SIMPLEX
        color = (0, 255, 0)
        
        detections = frame_data.faces_detections
        classes_data = frame_data.classes_data
        for coords, cls_data in zip(detections, classes_data):
            cv2.rectangle(frame, (coords.x_min, coords.y_min), (coords.x_min+coords.width, coords.y_min+coords.height), color, thickness)
            cv2.putText(
                frame, 
                f'#{cls_data.class_name}', 
                (coords.x_min, coords.y_min), 
                font, 
                fontScale, 
                color, 
                thickness, 
                cv2.LINE_AA)
        return frame

    @staticmethod
    def _serialize_frame_data(detections_data: DetectionData, classes_data: ClassificationData):
        detections = []
        pred_classes = []
        for det, cls in zip(detections_data, classes_data):
            if cls != None:
                detections.append(det)
                pred_classes.append(cls)
        frame_data = FrameData(detections, pred_classes)
        return frame_data