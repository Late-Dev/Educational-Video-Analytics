from abc import abstractmethod, ABC
from typing import List, Tuple
from dataclasses import dataclass
import math

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
            cropped = image[det_data.y_min:det_data.y_max, det_data.x_min:det_data.x_max]
            cropped_images.append(cropped)
        return cropped_images

    @staticmethod
    def _draw_predictions(frame: np.ndarray, frame_data: FrameData):

        color_map = {
            "спокойствие": np.array([178, 255, 54]),
            "радость": np.array([244, 183, 64]),
            "грусть": np.array([106, 150, 255]),
            "удивление": np.array([220, 140, 236]),
            "страх": np.array([0, 186, 136]),
            "отвращение": np.array([143, 64, 244]),
            "гнев": np.array([237, 46, 126]),
        }

        fontScale = 1
        thickness = 3
        font = cv2.FONT_HERSHEY_SIMPLEX
        color = (0, 255, 0)
        
        detections = frame_data.faces_detections
        face_emotions = frame_data.predicted_emotions
        
        for coords, emotions in zip(detections, face_emotions):
            emotion = max([(emotion.score, emotion.class_name) for emotion in emotions.emotions])
            rect_color = tuple(color_map[emotion[1]].tolist() + [min(1, math.ceil(emotion[0] * 10) / 10 * 2)])
            cv2.rectangle(frame, (coords.x_min, coords.y_min), (coords.x_max, coords.y_max), rect_color, thickness)
            rect_len = 50 if coords.tracking_id < 10 else 75
            cv2.rectangle(frame, (coords.x_min, coords.y_min-25), (coords.x_min+rect_len, coords.y_min), rect_color, -1)
            cv2.putText(frame, f'#{coords.tracking_id}', (coords.x_min, coords.y_min), font, fontScale, (0, 0, 0), 2, cv2.FILLED)

        emotion_average = dict()
        for data in face_emotions:
            for emotion in data.emotions:
                emotion_average.setdefault(emotion.class_name, 0) 
                emotion_average[emotion.class_name] += emotion.score / len(face_emotions)
        names = list(sorted(emotion_average.keys()))
        values = [emotion_average[i] for i in names]
        #colors = [(color_map[name] * value / 255 * 2).clip(0, 1) for name, value in zip(names, values)]
        colors = [(color_map[name] / 255).clip(0, 1) for name, value in zip(names, values)]
        
        matplotlib.rcParams.update({'font.size': 24})
        fig = Figure(figsize=(frame.shape[0] / 100, frame.shape[0] / 100), dpi=100)
        fig.set_tight_layout(True)
        canvas = FigureCanvas(fig)
        ax = fig.gca()
        for name, value, color in zip(names, values, colors):
            ax.barh([name], [value], color=[color], alpha=min(1, math.ceil(value * 10) / 10 * 2))
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
