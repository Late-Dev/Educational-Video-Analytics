from abc import abstractmethod, ABC
from typing import List, Tuple
from dataclasses import dataclass
from collections import Counter

import numpy as np
import cv2
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from infrastructure.interface import DetectionModel, DetectionData
from infrastructure.interface import ClassificationModel, ClassificationData


@dataclass
class FrameData:
    faces_detections: List[DetectionData]
    predicted_emotions: List[ClassificationData]


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
        
        for coords in detections:
            cv2.rectangle(frame, (coords.x_min, coords.y_min), (coords.x_min+coords.width, coords.y_min+coords.height), color, thickness)

        emotion_average = dict()
        face_emotions = frame_data.predicted_emotions
        for data in face_emotions:
            for emotion in data.emotions:
                emotion_average.setdefault(emotion.class_name, 0) 
                emotion_average[emotion.class_name] += emotion.score / len(face_emotions)
        names = list(sorted(emotion_average.keys()))
        values = [emotion_average[i] for i in names]
        
        matplotlib.rcParams.update({'font.size': 27})
        fig = Figure(figsize=(frame.shape[0] / 100, frame.shape[0] / 100), dpi=100)
        canvas = FigureCanvas(fig)
        ax = fig.gca()
        ax.barh(names, values)
        canvas.draw()       # draw the canvas, cache the renderer
        bar_image = np.frombuffer(canvas.tostring_rgb(), dtype='uint8').reshape((frame.shape[0], frame.shape[0], 3))
        return np.hstack([frame, bar_image])

    @staticmethod
    def _serialize_frame_data(detections_data: List[DetectionData], classes_data: ClassificationData):
        detections = []
        pred_classes = []
        for det, cls_data in zip(detections_data, classes_data):
            detections.append(det)
            pred_classes.append(cls_data)
        frame_data = FrameData(detections, pred_classes)
        return frame_data
