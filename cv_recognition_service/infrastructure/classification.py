import numpy as np
import cv2
import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image

from infrastructure.interface import ClassificationModel, ClassificationData, Emotion
from infrastructure.networks.dan import DAN 


class DummyClassifier(ClassificationModel):

    def __init__(self, model_path: str, conf_thresh: float) -> None:
        self.conf_thresh = conf_thresh
        self.model = self._load_model(model_path)

    def _load_model(self, model_path: str):
        def empty(image: np.ndarray):
            return ("happy", "0", 0.98)
        return empty
    
    def _image_preprocessing(self, image: np.ndarray) -> np.ndarray:
        return cv2.resize(image, (224, 224))


    def predict(self, image: np.ndarray):
        preprocessed_image = self._image_preprocessing(image)
        raw_predictions = self.model(preprocessed_image)
        predicted_cls, cls_id, conf = raw_predictions[0], raw_predictions[1], raw_predictions[2]
        
        if conf > self.conf_thresh:
            predictions = ClassificationData(predicted_cls, cls_id, conf)
            return predictions
        else:
            return None


class DanClassifier(ClassificationModel):

    def __init__(self, model_path: str, image_size = (224, 224)) -> None:
        self._image_size = image_size
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self._model = self._load_model(model_path)
        self._data_transforms = transforms.Compose(
            [
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
                ),
            ]
        )
        self._labels = (
            "спокойствие",
            "радость",
            "грусть",
            "удивление",
            "страх",
            "отвращение",
            "гнев",
        )


    def _load_model(self, model_path: str):
        model = DAN(num_head=4, num_class=7, pretrained=False)
        checkpoint = torch.load(model_path, map_location=self.device)
        model.load_state_dict(checkpoint["model_state_dict"], strict=True)
        model.to(self.device)
        model.eval()
        return model

    
    def _image_preprocessing(self, images_batch: np.ndarray) -> np.ndarray:
        result_batch = torch.zeros(len(images_batch), 3, *self._image_size)
        for i, image in enumerate(images_batch):
            image = self._data_transforms(Image.fromarray(image))
            image = image.view(3, *self._image_size)
            result_batch[i] = image
        result_batch = result_batch.to(self.device)
        return result_batch

    def _one_image_preprocess(self, image: np.ndarray):
        image = self._data_transforms(Image.fromarray(image))
        image = image.view(1, 3, *self._image_size)
        image = image.to(self.device)
        return image


    def predict(self, image: np.ndarray) -> ClassificationData:
        preprocessed_image = self._one_image_preprocess(image)
        with torch.no_grad():
            out, _, _ = self._model(preprocessed_image)
            probas = F.softmax(out, dim=1)
        pred = [Emotion(
                    class_name=self._labels[i],
                    class_id=i,
                    score=proba.item()
                )
                for i, proba in enumerate(probas[0])]
        cls_data = ClassificationData(pred)
        return cls_data

    def predict_batch(self, images_batch: np.ndarray):
        preprocessed_image = self._image_preprocessing(images_batch)

        with torch.no_grad():
            out, _, _ = self._model(preprocessed_image)
            probas_batch = F.softmax(out, dim=1)

        predictions = [
            [
                Emotion(
                    class_name=self._labels[i],
                    class_id=i,
                    score=proba.item()
                )
                for i, proba in enumerate(probas)
            ]
            for probas in probas_batch
        ]
        return predictions
        