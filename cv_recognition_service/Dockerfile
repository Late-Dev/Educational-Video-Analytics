FROM pytorch/pytorch:1.11.0-cuda11.3-cudnn8-runtime
WORKDIR /cv_recognition_service

COPY requirements.txt $WORKDIR

RUN apt-get update && apt-get clean && apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install -U pip && \
    pip install jupyter && \
    pip install -r requirements.txt --no-cache-dir

RUN apt-get install unzip && \
    gdown --id 1dv-AnbAEbdtR_ZrmmS0qoV_YBFD7tSZV -O ./ && \
    unzip models.zip && \
    rm -f models.zip*

COPY . $WORKDIR

# CMD jupyter notebook --ip 0.0.0.0 --port 9988 --allow-root --NotebookApp.token=""
ENTRYPOINT [ "python", "main.py" ]