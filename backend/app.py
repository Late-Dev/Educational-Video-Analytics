from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder

from database import add_video_data
from models import VideoSchema

app = FastAPI()


@app.get("/")
async def healthcheck():
    return "I am alive!"

@app.post("/add_video")
async def add_video(video: VideoSchema):
    video = jsonable_encoder(video)
    await add_video_data(video)
    return "Success"
