import os
from enum import Enum
import motor.motor_asyncio

mongo_host = os.environ["MONGO_HOST"]
MONGO_DETAILS = f"mongodb://admin:admin@{mongo_host}:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.data

lesson_videos_collection = database.get_collection("lesson_videos")


class StatusEnum(str, Enum):
    uploaded = "uploaded"
    processing = "processing"
    ready = "ready"
    error = "error"


async def add_video_data(video):
    video['status'] = StatusEnum.uploaded
    await lesson_videos_collection.insert_one(video)


async def get_video_list_data():
    videos = []
    async for video in lesson_videos_collection.find():
        video['_id'] = str(video['_id'])
        videos.append(video)
    return videos
