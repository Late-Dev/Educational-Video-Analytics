from typing import Optional
from datetime import datetime
from pydantic import BaseModel, AnyUrl


class VideoSchema(BaseModel):
    url: AnyUrl
    school_class: str
    teacher: str
    subject: str
    lesson_start_time: datetime

    class Config:
        schema_extra = {
            "example": {
                "url": "s3://12345",
                "school_class": "7А",
                "teacher": "Иванова А.А.",
                "subject": "Математика",
                "lesson_start_time": "2022-06-01T00:18:31+00:00"
            }
        }
