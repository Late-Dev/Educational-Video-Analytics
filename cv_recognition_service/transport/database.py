from asyncio import tasks
import os
from enum import Enum
from pymongo import MongoClient


class StatusEnum(str, Enum):
    uploaded = "uploaded"
    processing = "processing"
    ready = "ready"
    error = "error"


mongo_host = os.environ["MONGO_HOST"]
MONGO_DETAILS = f"mongodb://admin:admin@{mongo_host}:27017"

client = MongoClient(MONGO_DETAILS)

database = client.data

lesson_videos_collection = database.get_collection("lesson_videos")


def find_task(field: dict):
    try:
        task = lesson_videos_collection.find_one(field)
        return task
    except:
        return False


def update_task(task: dict, set: dict):
    try:
        lesson_videos_collection.update_one({"_id": task["_id"]}, {"$set": set})
        return True
    except:
        return False


if __name__ == "__main__":
    task = find_task({"status": StatusEnum.uploaded})
    print(task)
    print()

    if update_task(task, {"preview": "http://test.preview-url", "status": StatusEnum.processing}):
        task = find_task({"status": StatusEnum.processing})
        print(task)
