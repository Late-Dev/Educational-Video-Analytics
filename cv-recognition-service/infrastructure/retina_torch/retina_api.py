import logging
from pathlib import Path

import torch
import torch.backends.cudnn as cudnn
import numpy as np

from .rcnn_torch.retinaface import RetinaFace  # noqa
from .rcnn_torch.layers.functions.prior_box import PriorBox  # noqa
from .utils.box_utils import decode, decode_landm  # noqa
from .utils.nms.py_cpu_nms import py_cpu_nms  # noqa
from .utils import face_align  # noqa

CURRENT_DIR = Path(__file__).parent


class RetinaDetector:
    def __init__(self, config):
        self.config = config
        self.log = logging.getLogger(__name__)
        self.log.setLevel(self.config["logging"]["set_level"])
        self.model_config = config["detector"]["cfg_re50"]
        # self.model_config = config['detector']['cfg_mnet']

        self.model_path = (
            CURRENT_DIR / "../../models/face_search" / self.model_config["model_path"]
        )
        self.model = RetinaFace(cfg=self.model_config, phase="test")
        self.detector = self.load_model(self.model)
        self.detector.eval()
        # self.log.info("Finished loading model!")

        cudnn.benchmark = True
        self.device = torch.device("cuda" if self.config["gpu"] else "cpu")
        self.detector = self.detector.to(self.device)

        self.resize = 1

    def check_keys(self, model, pretrained_state_dict):
        ckpt_keys = set(pretrained_state_dict.keys())
        model_keys = set(model.state_dict().keys())
        used_pretrained_keys = model_keys & ckpt_keys
        unused_pretrained_keys = ckpt_keys - model_keys
        missing_keys = model_keys - ckpt_keys
        # self.log.info(f"Missing keys:{len(missing_keys)}")
        # self.log.info(f"Unused checkpoint keys:{len(unused_pretrained_keys)}")
        # self.log.info("Used keys:{}".format(len(used_pretrained_keys)))
        assert len(used_pretrained_keys) > 0, "load NONE from pretrained checkpoint"
        return True

    def remove_prefix(self, state_dict, prefix):
        """Old style model is stored with all names of parameters sharing common prefix 'module.'"""
        # self.log.info(f"remove prefix '{prefix}'")
        f = lambda x: x.split(prefix, 1)[-1] if x.startswith(prefix) else x
        return {f(key): value for key, value in state_dict.items()}

    def load_model(self, model):
        # self.log.info(f"Loading pretrained model from {self.model_path}")
        if not self.config["gpu"]:
            pretrained_dict = torch.load(
                self.model_path, map_location=lambda storage, loc: storage
            )
        else:
            device = torch.cuda.current_device()
            pretrained_dict = torch.load(
                self.model_path, map_location=lambda storage, loc: storage.cuda(device)
            )
        if "state_dict" in pretrained_dict.keys():
            pretrained_dict = self.remove_prefix(
                pretrained_dict["state_dict"], "module."
            )
        else:
            pretrained_dict = self.remove_prefix(pretrained_dict, "module.")
        self.check_keys(model, pretrained_dict)
        model.load_state_dict(pretrained_dict, strict=False)
        return model

    def detect(self, image):
        np_img = np.float32(image)
        im_height, im_width, _ = image.shape
        scale = torch.Tensor(
            [np_img.shape[1], np_img.shape[0], np_img.shape[1], np_img.shape[0]]
        )
        np_img -= (104, 117, 123)
        np_img = np_img.transpose(2, 0, 1)
        np_img = torch.from_numpy(np_img).unsqueeze(0)
        np_img = np_img.to(self.device)
        scale = scale.to(self.device)

        loc, conf, landmarks = self.detector(np_img)  # forward pass

        priorbox = PriorBox(self.model_config, image_size=(im_height, im_width))
        priors = priorbox.forward()
        priors = priors.to(self.device)
        prior_data = priors.data
        boxes = decode(loc.data.squeeze(0), prior_data, self.model_config["variance"])
        boxes = boxes * scale / self.resize
        boxes = boxes.cpu().numpy()
        scores = conf.squeeze(0).data.cpu().numpy()[:, 1]
        landmarks = decode_landm(
            landmarks.data.squeeze(0), prior_data, self.model_config["variance"]
        )
        scale1 = torch.Tensor(
            [
                np_img.shape[3],
                np_img.shape[2],
                np_img.shape[3],
                np_img.shape[2],
                np_img.shape[3],
                np_img.shape[2],
                np_img.shape[3],
                np_img.shape[2],
                np_img.shape[3],
                np_img.shape[2],
            ]
        )
        scale1 = scale1.to(self.device)
        landmarks = landmarks * scale1 / self.resize
        landmarks = landmarks.cpu().numpy()

        # ignore low scores
        inds = np.where(scores > self.config["confidence_threshold"])[0]
        boxes = boxes[inds]
        landmarks = landmarks[inds]
        scores = scores[inds]

        # keep top-K before NMS
        order = scores.argsort()[::-1][: self.config["top_k"]]
        boxes = boxes[order]
        landmarks = landmarks[order]
        scores = scores[order]

        # do NMS
        dets = np.hstack((boxes, scores[:, np.newaxis])).astype(np.float32, copy=False)
        keep = py_cpu_nms(dets, self.config["nms_threshold"])
        # keep = nms(dets, args.nms_threshold,force_cpu=args.cpu)
        dets = dets[keep, :]
        landmarks = landmarks[keep]

        # keep top-K faster NMS
        dets = dets[: self.config["keep_top_k"], :]
        landmarks = landmarks[: self.config["keep_top_k"], :]

        return dets, landmarks

    def get_faces(self, img):
        dets, landmarks = self.detect(img)
        coordinate_faces = list(
            map(lambda x: [int(x[0]), int(x[1]), int(x[2]), int(x[3]), x[4]], dets)
        )
        # faces = [
        #     img[int(y1) : int(y2), int(x1) : int(x2)] for x1, y1, x2, y2, _ in dets
        # ]
        faces = [
            face_align.norm_crop(img, landmark)
            for landmark in np.reshape(landmarks, (landmarks.shape[0], 5, 2))
        ]
        # self.log.info(f"Retina detect {len(align_faces)} faces")
        return coordinate_faces, faces
