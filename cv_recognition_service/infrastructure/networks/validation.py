import json
from typing import Any, Tuple
from pathlib import Path
import sys

from pyrsistent import m

sys.path.append(
    "/home/and/projects/hacks/hacks_ai_ural_emotion_recognition/APP/Educational-Video-Analytics/cv_recognition_service/infrastructure/networks"
)

import cv2
import torch
import numpy as np
import pandas as pd
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from PIL import Image
from tqdm.auto import tqdm
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score
from dan import DAN
from torchvision import models

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
BATCH_SIZE = 64

eng2ru_map = {
    "anger": "гнев",
    "disgust": "отвращение",
    "fear": "страх",
    "happy": "радость",
    "neutral": "спокойствие",
    "sad": "грусть",
    "surprise": "удивление",
}


class EmotionTestDataset(Dataset):
    def __init__(self, data_folder, img_shape, labels) -> None:
        super().__init__()
        data_folder = Path(data_folder)
        self._labels = labels

        label2id = {label: i for i, label in enumerate(self._labels)}
        self._samples = [
            [str(img_p), label2id[eng2ru_map[label.name]]]
            for label in data_folder.iterdir()
            for img_p in label.iterdir()
        ]
        print(label2id)

        self.transform = transforms.Compose(
            [
                transforms.Resize(img_shape),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
                ),
            ]
        )

    def __len__(self) -> int:
        return len(self._samples)

    def __getitem__(self, idx: int) -> Tuple[Any, Any]:
        image_p, target = self._samples[idx]
        image = cv2.cvtColor(cv2.imread(str(image_p)), cv2.COLOR_BGR2RGB)

        if self.transform is not None:
            image = Image.fromarray(image)
            image = self.transform(image)

        return image, target


def load_model(model_path, backbone, shape, device=DEVICE):
    model = DAN(backbone=backbone, conv_size=shape)
    model.load_state_dict(
        torch.load(model_path, map_location=device)["model_state_dict"], strict=True
    )
    model.to(device)
    model.eval()
    return model


def validate(
    model,
    model_name,
    device=DEVICE,
    data_path="datasets/AffectNet/val",
    save_name="metric",
    img_shape=(224, 224),
    labels=(
        "спокойствие",
        "радость",
        "грусть",
        "удивление",
        "страх",
        "отвращение",
        "гнев",
    ),
):
    print(f"{save_name}.csv")

    data_path = Path(data_path)
    dataset = EmotionTestDataset(data_path, img_shape=img_shape, labels=labels)
    dataloader = DataLoader(
        dataset, batch_size=BATCH_SIZE, shuffle=False, pin_memory=True
    )

    labels = list(labels)
    metrics = {
        "all_classes": {
            "true_positive": 0,
            "false_positive": 0,
            "false_negative": 0,
        },
        **{
            label: {
                "true_positive": 0,
                "false_positive": 0,
                "false_negative": 0,
            }
            for label in labels
        },
    }

    all_predictions = []
    all_targets = []

    for batch, targets in tqdm(dataloader):
        with torch.no_grad():
            batch = batch.to(device)
            targets = targets.cpu().numpy()

            if model_name == "dan":
                out, _, _ = model(batch)

            probas = F.softmax(out, dim=1).cpu().numpy()
            predicts = np.array([proba.argmax() for proba in probas])

            all_predictions += predicts.tolist()
            all_targets += targets.tolist()

    all_predictions = np.array(all_predictions)
    all_targets = np.array(all_targets)
    for label in labels:
        label_id = labels.index(label)
        for p, t in zip(all_predictions, all_targets):
            if t == label_id:
                if p == t:
                    metrics["all_classes"]["true_positive"] += 1
                    metrics[label]["true_positive"] += 1
                elif p != t:
                    metrics["all_classes"]["false_positive"] += 1
                    metrics[label]["false_positive"] += 1
            else:
                if p == label_id:
                    metrics["all_classes"]["false_negative"] += 1
                    metrics[label]["false_negative"] += 1

    for label in labels + ["all_classes"]:
        metrics[label]["precision"] = metrics[label]["true_positive"] / (
            metrics[label]["true_positive"] + metrics[label]["false_positive"] + 1e-8
        )
        metrics[label]["recall"] = metrics[label]["true_positive"] / (
            metrics[label]["true_positive"] + metrics[label]["false_negative"] + 1e-8
        )
        metrics[label]["f1_score"] = (
            2
            * metrics[label]["precision"]
            * metrics[label]["recall"]
            / (metrics[label]["precision"] + metrics[label]["recall"] + 1e-8)
        )

    # metrics["all_classes"]["f1_macro"] = f1_score(
    #     all_targets, all_predictions, average="macro"
    # )
    # metrics["all_classes"]["f1_micro"] = f1_score(
    #     all_targets, all_predictions, average="micro"
    # )
    # metrics["all_classes"]["precision_micro"] = precision_score(
    #     all_targets, all_predictions, average="micro"
    # )

    pd.DataFrame(metrics, columns=["all_classes", *labels]).to_csv(f"{save_name}.csv")


if __name__ == "__main__":
    model_paths = [
        "/home/and/projects/hacks/hacks_ai_ural_emotion_recognition/emotions-training/experiments/DAN/checkpoints/affecnet7_epoch6_acc0.6569.pth",
        "/home/and/projects/hacks/hacks_ai_ural_emotion_recognition/emotions-training/experiments/DAN/checkpoints/rafdb_epoch21_acc0.897_bacc0.8275.pth",
        "/home/and/projects/hacks/hacks_ai_ural_emotion_recognition/emotions-training/experiments/DAN/checkpoints/affecnet_res34_epoch17_acc0.7498.pth",
        "/home/and/projects/hacks/hacks_ai_ural_emotion_recognition/emotions-training/experiments/DAN/checkpoints/affecnet_eff_b3_acc0.7316.pth",
    ]
    backbones = [
        models.resnet18(),
        models.resnet18(),
        models.resnet34(),
        models.efficientnet_b3(),
    ]
    shapes = [None, None, None, 1536]
    img_shapes = [224, 224, 224, 300]

    test_data = [
        "/home/and/projects/hacks/hacks_ai_ural_emotion_recognition/emotions-training/experiments/DAN/datasets/AffectNet/val",
        # "/home/and/projects/hacks/hacks_ai_ural_emotion_recognition/emotions-training/experiments/DAN/datasets/fer/test",
    ]

    labels = [
        (
            "спокойствие",
            "радость",
            "грусть",
            "удивление",
            "страх",
            "отвращение",
            "гнев",
        ),
        (
            "удивление",
            "страх",
            "отвращение",
            "радость",
            "грусть",
            "гнев",
            "спокойствие",
        ),
        (
            "гнев",
            "отвращение",
            "страх",
            "радость",
            "спокойствие",
            "грусть",
            "удивление",
        ),
        (
            "гнев",
            "отвращение",
            "страх",
            "радость",
            "спокойствие",
            "грусть",
            "удивление",
        ),
        (
            "гнев",
            "отвращение",
            "страх",
            "радость",
            "спокойствие",
            "грусть",
            "удивление",
        ),
    ]

    for model_p, backbone, shape, img_shape, lbls in tqdm(
        zip(model_paths, backbones, shapes, img_shapes, labels), total=4
    ):
        model_p = Path(model_p)
        model = load_model(model_p, backbone, shape)

        for data_p in test_data:
            data_p = Path(data_p)
            validate(
                model,
                "dan",
                img_shape=img_shape,
                data_path=data_p,
                save_name=f"metric_{data_p.parent.name}_{model_p.name[:-4]}",
                labels=lbls,
            )
