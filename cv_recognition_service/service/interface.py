from abc import abstractmethod, ABC
from typing import List, Tuple
from dataclasses import dataclass

import numpy as np
import cv2

from cv_recognition_service.infrastructure.interface import DetectionModel, DetectionData
from cv_recognition_service.infrastructure.interface import ClassificationModel, ClassificationData


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
    def _crop_images(image: np.ndarray, contours: List[Tuple(int, int, int, int)]):
        cropped_images = []
        for cnt in contours:
            x, y, w, h = cnt
            cropped = image[y:y+h, x:x+w]
            cropped_images.append(cropped)
        return cropped_images

    @staticmethod
    def _draw_predictions(frame: np.ndarray, predictions: List[FrameData]):
        fontScale = 1
        thickness = 3
        font = cv2.FONT_HERSHEY_SIMPLEX
        color = (0, 255, 0)
        
        for frame_data in predictions:
            detections = frame_data.faces_detections
            classes_data = frame_data.classes_data
            for coords, cls_data in zip(detections, classes_data):
                cv2.rectangle(frame, (coords.x_min, coords.y_min), (coords.x_max, coords.y_max), color, thickness)
                cv2.putText(
                    frame, 
                    f'#{cls_data.class_name}', 
                    (detections.x_min, detections.y_min), 
                    font, 
                    fontScale, 
                    color, 
                    thickness, 
                    cv2.LINE_AA)
        return frame