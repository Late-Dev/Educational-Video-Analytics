from cv-recognition-service.infrastructure.interface import DetectionModel, DetectionData
from cv-recognition-service.infrastructure.interface import ClassificationModel, ClassificationData
from cv-recognition-service.service.interface import BaseService, FrameData


class DummyEmotionService(BaseService):

    def __init__(self) -> None:
        def __init__(self, detection_model, classification_model, det_threshold=0.9, cls_thresh=0.9):
            self.detection_model = detection_model
            self.classification_model = classification_model

        