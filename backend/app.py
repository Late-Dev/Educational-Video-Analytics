from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

from database import add_video_data
from models import VideoSchema

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8081",
    "http://http://127.0.0.1:8080"
    "http://http://127.0.0.1:8081"
    "http://http://127.0.0.1"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def healthcheck():
    return "I am alive!"


@app.post("/add_video")
async def add_video(video: VideoSchema):
    video = jsonable_encoder(video)
    await add_video_data(video)
    return "Success"
