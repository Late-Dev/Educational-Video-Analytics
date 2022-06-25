import os

from transport.database import StatusEnum, update_task
from transport.s3 import upload_file
from workers.video import create_preview_image, process_video


def upload_preview_handler(filepath: str, task: dict):
    url="http://minio:9000/preview-images/"
    # create preview img
    preview_filepath = create_preview_image(filepath)
    # upload preview to bucket
    filename = os.path.basename(preview_filepath)
    res = upload_file(file_path=preview_filepath, url=url)
    # update status in db
    if res:
        update_task(task, {"status": StatusEnum.processing, "preview-url": f"{url}{filename}"})
    else:
        raise("Create preview error")


def process_video_handler(filepath: str, task: dict):
    # start video processing
    output_filepath, bar_data, line_data = process_video(filepath)
    print(line_data)
    # upload processed file to bucket
    url = "http://minio:9000/processed-videos/"
    filename = os.path.basename(output_filepath)
    res = upload_file(output_filepath, url)
    if res:
        update_task(task, {"status": StatusEnum.ready, "bar_data": bar_data, "line_data": line_data})
    else:
        update_task(task, {"status": StatusEnum.error})
