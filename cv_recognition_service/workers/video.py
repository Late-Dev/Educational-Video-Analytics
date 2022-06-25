import os
from typing import List

import cv2
from tqdm import trange

from service.interface import BaseService
from building import build_emotion_service


service = build_emotion_service()


def process_video(video_path: str):
    capture = cv2.VideoCapture(video_path)
    length = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    # width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    width = 2000 #TODO Fix this
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fps = 10
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out_path = f'output/{os.path.basename(video_path)}'
    writer = cv2.VideoWriter(out_path, fourcc, fps, (width, height))

    for _ in trange(length):
        ret, frame = capture.read()
        if frame is None:
            break
        new_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        plotted_frame, frame_data = service.process_frame(new_frame)
        writer.write(cv2.cvtColor(plotted_frame, cv2.COLOR_RGB2BGR))

    writer.release() 
    capture.release()
    return out_path


def create_preview_image(video_path: str):
    capture = cv2.VideoCapture(video_path)
    length = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    imagename = f"{str(os.path.basename(video_path)).split('.')[-2]}.jpg"
    out_path = f'output/{imagename}'
    for _ in range(15):
        if _ == 14:
            ret, frame = capture.read()
            if frame is None:
                break
            new_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            plotted_frame = service.process_frame(new_frame)
            cv2.imwrite(out_path, cv2.cvtColor(plotted_frame, cv2.COLOR_BGR2RGB))
            return out_path
