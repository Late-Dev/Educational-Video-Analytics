import os
from typing import List
from random import shuffle

import av
import cv2
import numpy as np
from tqdm import trange
import torch
import torchvision

from service.interface import BaseService
from building import build_emotion_service

color_map = {
            "спокойствие": np.array([178, 255, 54]),
            "радость": np.array([244, 183, 64]),
            "грусть": np.array([106, 150, 255]),
            "удивление": np.array([220, 140, 236]),
            "страх": np.array([0, 186, 136]),
            "отвращение": np.array([143, 64, 244]),
            "гнев": np.array([237, 46, 126]),
        }

service = build_emotion_service()


def process_video(video_path: str):

    capture = cv2.VideoCapture(video_path)
    length = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    # width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    width = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)) + int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fps = 10
    #fourcc = cv2.VideoWriter_fourcc(*'h264')
    out_path = f'output/{os.path.basename(video_path)}'
    #writer = cv2.VideoWriter(out_path, fourcc, fps, (width, height))

    emotion_average = dict()

    names = [name.strip() for name in open('names.txt').readlines()]
    shuffle(names)
    line_data = {}
    
    #videoframes = []
    video_codec = "libx264"
    options= None
    audio_array = None
    audio_fps = None
    audio_codec= None
    audio_options = None

    with av.open(out_path, mode="w") as container:
        stream = container.add_stream(video_codec, rate=fps)
        stream.width = width
        stream.height = height
        stream.pix_fmt = "yuv420p" if video_codec != "libx264rgb" else "rgb24"
        stream.options = options or {}

        length = 1000
        for i in trange(length):
            ret, frame = capture.read()
            if frame is None:
                break
            if i % 10 == 0:
                continue
            new_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            plotted_frame, frame_data = service.process_frame(new_frame, frames_to_analize=15)
            #writer.write(cv2.cvtColor(plotted_frame, cv2.COLOR_RGB2BGR))
            #videoframes.append(plotted_frame)

            detections = frame_data.faces_detections
            face_emotions = frame_data.predicted_emotions
            
            for data in face_emotions:
                for emotion in data.emotions:
                    emotion_average.setdefault(emotion.class_name, []) 
                    emotion_average[emotion.class_name].append(emotion.score)

            for coords, emotions in zip(detections, face_emotions):

                for emotion in data.emotions:
                    emotion_average.setdefault(emotion.class_name, 0) 
                    line_data.setdefault(names[coords.tracking_id], {}).setdefault(emotion.class_name, []).append(emotion.score)


            frame = av.VideoFrame.from_ndarray(plotted_frame, format="rgb24")
            frame.pict_type = "NONE"
            for packet in stream.encode(frame):
                container.mux(packet)

        # Flush stream
        for packet in stream.encode():
            container.mux(packet)


    names = list(sorted(emotion_average.keys()))
    values = [np.mean(emotion_average[i]) for i in names]

    bar_data = {
        'names': names,
        'values': values,
    }

    all_students = {}
    for emotion in names:
        all_students[emotion] = [0] * length
        for student in line_data:
            for i, value in enumerate(line_data[student][emotion]):
                all_students[emotion][i] += value / len(line_data)

    line_data['Весь класс'] = all_students
    #writer.release() 
    #torchvision.io.write_video(out_path, torch.from_numpy(np.array(videoframes)), fps=5)
    capture.release()
    return out_path, bar_data, line_data


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
