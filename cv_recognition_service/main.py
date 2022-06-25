import os
from time import sleep
from pathlib import Path

from transport.database import StatusEnum, find_task, update_task
from transport.s3 import download_file
from handlers import process_video_handler, upload_preview_handler


def clean_tmp_dirs(dirs=['/cv_recognition_service/tmp/', '/cv_recognition_service/tmp/output']):
    for dir in dirs:
        [f.unlink() for f in Path(dir).glob("*") if f.is_file()] 


def main(sleep_range: float):
    while True:
        task = find_task({"status": StatusEnum.uploaded})
        if task:
            print(task)
            file_url = task['url']
            try:
                file_path = download_file(file_url)
                update_task(task, {"status": StatusEnum.processing})
            except Exception as err:
                error = f"File {file_url} not loaded \n Error: {err}"
                print(error)
                update_task(task, {"status": StatusEnum.error, "error": error})
                continue
            # call preview handler
            # try:
            #     upload_preview_handler(file_path, task)
            # except Exception as err:
            #     error = f"Error while creating preview image for file: {file_url} \n Error: {err}"
            #     print(error)
            #     update_task(task, {"status": StatusEnum.error, "error": error})
            #     continue
            # call processing handler
            try:
                process_video_handler(file_path, task)
                clean_tmp_dirs()
            except Exception as err:
                error = f"Error while processing video file: {file_url} \n Error: {err}"
                update_task(task, {"status": StatusEnum.error})
                continue
        else:
            print(f"no task, sleeping {sleep_range}s ...")
            sleep(sleep_range)


    
if __name__ == "__main__":
    os.makedirs('/cv_recognition_service/tmp/', exist_ok=True)
    os.makedirs('/cv_recognition_service/output/', exist_ok=True)

    main(sleep_range=5.0)
