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
        self._last_frames_data: List[FrameData] = []

    def _match_frames_data(self, current_frame_data: FrameData):
        if len(self._last_frames_data) == 1:
            return current_frame_data

        cur_track_ids = [
            det_data.tracking_id for det_data in current_frame_data.faces_detections
        ]
        cur_emotions_list = [
            [predict.emotions] for predict in current_frame_data.predicted_emotions
        ]

        for frame_data in self._last_frames_data:
            track_ids = [
                det_data.tracking_id for det_data in frame_data.faces_detections
            ]
            emotions_list = [
                predict.emotions for predict in frame_data.predicted_emotions
            ]
            for track_id, emotions in zip(track_ids, emotions_list):
                if track_id in cur_track_ids:
                    idx = cur_track_ids.index(track_id)
                    cur_emotions_list[idx].append(emotions)

        for i, emotions_list_list in enumerate(cur_emotions_list):  # loop for persons
            # emotions_list_list: List[List[Emotion]]
            for j, emotion_list in enumerate(emotions_list_list):  # loop for frames
                # emotion_list: List[Emotion]
                for k, emotion in enumerate(emotion_list):  # loop for emotions
                    current_frame_data.predicted_emotions[i].emotions[
                        k
                    ].score += emotion.score

                for k, emotion in enumerate(emotion_list):  # loop for emotions
                    current_frame_data.predicted_emotions[i].emotions[k].score /= len(
                        emotion_list
                    )

        self._last_frames_data.append(current_frame_data)

        return current_frame_data

    def _update_frame_data(self, current_frame_data: FrameData, frames_to_analize: int):
        if len(self._last_frames_data) >= frames_to_analize:
            self._last_frames_data[:] = self._last_frames_data[1:]

        current_frame_data = self._match_frames_data(current_frame_data)

        return current_frame_data

    def process_frame(self, frame: np.ndarray, frames_to_analize: int = 1) -> FrameData:
        detections_data = self.detection_model.detect(frame)
        classes_data = [
            self.classification_model.predict(dd.face) for dd in detections_data
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
        frame_data = self._update_frame_data(frame_data, frames_to_analize)
        plotted_frame = self._draw_predictions(frame, frame_data)
        return plotted_frame
