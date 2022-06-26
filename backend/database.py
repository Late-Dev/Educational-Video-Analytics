import os
from enum import Enum
import motor.motor_asyncio
from bson.objectid import ObjectId

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
        if 'bar_data' in video:
            del video['bar_data']
        if 'line_data' in video:
            del video['line_data']
        videos.append(video)
    return videos


async def get_video_card_data(_id):
    card = await lesson_videos_collection.find_one({'_id': ObjectId(_id)})
    if card is not None:
        card['_id'] = str(card['_id'])
    return card


def mean(x):
    return sum(x) / len(x)

async def get_analytics_data(filter_type: str=None, filter_value: str=None, group:str=None):
    names = [ "гнев", "грусть", "отвращение", "радость", "спокойствие", "страх", "удивление" ]
    if filter_type is None and group is None:
        values = [0 for _ in names]

        count = 0
        async for video in lesson_videos_collection.find():
            for i, value in enumerate(video['bar_data']['values']):
                values[i] += value
            count += 1

        for i in range(len(values)):
            values[i] /= count

        result = [{
            'title': '',
            'names': names,
            'values': values,
        }]

    elif filter_type is not None and filter_type != 'student' and group is None:
        card = await lesson_videos_collection.find_one({filter_type: filter_value})
        result = [card['bar_data']]
    elif filter_type is not None and filter_type == 'student' and group is None:
        result = []
        async for video in lesson_videos_collection.find():
            if filter_value in video['line_data']:
                values = [mean(video['line_data'][filter_value][i]) for i in names]
                result = [{
                    'title': '',
                    'names': names,
                    'values': values,
                }]
                break            
        

    elif filter_type is None and group is not None and group != 'student':

        used = set()
        result = []
        async for video in lesson_videos_collection.find():
            if video[group] not in used:
                used.add(video[group])
            bar = video['bar_data']
            bar['title'] = video[group]
            result.append(bar)

    elif filter_type is None and group is not None and group == 'student':
        used = set()
        result = []
        async for video in lesson_videos_collection.find():
            for student in video['line_data']:
                if student not in used and student != "Весь класс":
                    used.add(student)
                    values = [mean(video['line_data'][student][i]) for i in names]
                    bar = {
                        'names': names,
                        'values': values,
                    }
                    bar['title'] = student
                    result.append(bar)
    elif filter_type is not None and filter_type != 'student' and group is not None and group != 'student':
        card = await lesson_videos_collection.find_one({filter_type: filter_value})
        bar = card['bar_data']
        bar['title'] = card[group]
        result = [bar]
    elif filter_type is not None and filter_type != 'student' and group is not None and group == 'student':
        video = await lesson_videos_collection.find_one({filter_type: filter_value})
        result = []
        for student in video['line_data']:
            if student == "Весь класс":
                continue
            values = [mean(video['line_data'][student][i]) for i in names]
            bar = {
                'title': student,
                'names': names,
                'values': values,
            }
            result.append(bar)
    elif filter_type is not None and filter_type == 'student' and group is not None:
        used = set()
        result = []
        async for video in lesson_videos_collection.find():
            if student in video['line_data'] and video[group] not in used:
                used.add(video[group])
                values = [mean(video['line_data'][student][i]) for i in names]
                bar = {
                    'names': names,
                    'values': values,
                }
                bar['title'] = video[group]
                result.append(bar)

    return result
