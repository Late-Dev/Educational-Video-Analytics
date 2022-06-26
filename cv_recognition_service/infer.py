import os
import json
import argparse
from pathlib import Path
from typing import List, Optional

import cv2
import numpy as np
from tqdm import tqdm
from tqdm import trange


from infrastructure.interface import DetectionModel
from infrastructure.interface import ClassificationModel
from infrastructure.tracking.wrapper import DeepsortTracker
from service.interface import BaseService, FrameData
from infrastructure.detection import RetinaTorchDetector
from infrastructure.classification import DanClassifier


class InferFilesService(BaseService):
    def __init__(
        self,
        detection_model: DetectionModel,
        classification_model: ClassificationModel,
        tracking_model: DeepsortTracker,
        det_threshold=0.9,
        cls_thresh=0.9,
    ) -> None:
        self.detection_model = detection_model
        self.tracking_model = tracking_model
        self.classification_model = classification_model
        self.det_threshold = det_threshold
        self.cls_thresh = cls_thresh
        self._labels = (
            "neutral",
            "happy",
            "sadness",
            "surprise",
            "fear",
            "disgust",
            "anger",
        )
        self.id2label = {i: label for i, label in enumerate(self._labels)}

    def process_frame(self, frame: np.ndarray) -> FrameData:
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
        plotted_frame = self._draw_predictions(frame, frame_data)

        # ONLY ONE FACE
        emotions_probas = None
        if frame_data.predicted_emotions:
            emotions_probas = np.array(
                [
                    emotion.score
                    for emotion in frame_data.predicted_emotions[0].emotions
                ],
                dtype=np.float32,
            )
        return plotted_frame, emotions_probas

    def process(self, input_dir: Path, output_dir: Path = Path("output")):
        output_dir.mkdir(exist_ok=True)

        video_paths = list(input_dir.iterdir())
        results = {}
        print(video_paths)
        for video_path in tqdm(video_paths, leave=False):
            video_probas = np.array([0.0 for _ in range(7)])
            capture = cv2.VideoCapture(str(video_path))
            length = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
            # width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            width = 2000
            height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

            fps = 10
            fourcc = cv2.VideoWriter_fourcc(*"h264")
            writer = cv2.VideoWriter(
                str(output_dir / video_path.name), fourcc, fps, (width, height)
            )

            for _ in trange(length):
                ret, frame = capture.read()
                if frame is None:
                    break
                new_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                plotted_frame, emotions_probas = self.process_frame(new_frame)
                if emotions_probas is not None:
                    video_probas += emotions_probas

                writer.write(cv2.cvtColor(plotted_frame, cv2.COLOR_RGB2BGR))

            writer.release()
            capture.release()

            emotion = self.id2label[video_probas.argmax()]
            results[str(video_path)] = emotion

            with open(output_dir / "results.json", "w") as f:
                json.dump(results, f)


def setup_parser():
    parser = argparse.ArgumentParser(description="Emotion Recognition Script")
    parser.add_argument(
        "-i",
        "--input-dir",
        type=Path,
        help="Path to the folder with video files",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        help="Path to the folder to save answers",
    )
    return parser


def main():
    parser = setup_parser()
    arguments = parser.parse_args()

    detector = RetinaTorchDetector(
        model_path="infrastructure/retina_torch/config.json", conf_thresh=0.9
    )
    classifier = DanClassifier(model_path="models/affecnet7_epoch6_acc0.6569.pth")
    tracker = DeepsortTracker("models/mars-small128.pb")

    service = InferFilesService(detector, classifier, tracker)
    service.process(arguments.input_dir, arguments.output_dir)


if __name__ == "__main__":
    main()
