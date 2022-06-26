from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

from database import add_video_data, get_video_list_data, get_video_card_data, get_analytics_data
from models import VideoSchema

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8081",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8081",
    "http://127.0.0.1",
    "http://10.10.67.125",
    "http://10.10.67.125:8080",
    "http://10.10.67.125:8081",
    "http://185.175.44.146",
    "http://185.175.44.146:8080",
    "http://185.175.44.146:8081"
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


@app.get("/get_video_list")
async def get_video_list():
    result = await get_video_list_data()
    return result


@app.get("/get_video_card")
async def get_video_card(_id: str):
    result = await get_video_card_data(_id)
    return result if result is not None else {'Error': 'Video not found'}

@app.get("/get_analytics")
async def get_analytics(filter_type: str=None, filter_value: str=None, group:str=None):
    result = await get_analytics_data(filter_type, filter_value, group)
    return result
