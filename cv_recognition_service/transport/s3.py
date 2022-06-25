import requests
import base64


def read_file_as_bytes(file_path: str):
    with open(file_path, "rb") as image_file:
        file_bytes = image_file.read()
    return file_bytes


def download_file(url: str, save_path: str = 'tmp/'):
    file_path = f"{save_path}{url.split('/')[-1]}"
    r = requests.get(url, verify=False)
    if r.ok:
        with open(file_path, "wb") as file:
            file.write(r.content)
        return file_path
    else:
        raise("Couldnt download file")


def upload_file(file_path: str, url: str):
    """
    Put files on bucket
    """
    file_bytes = read_file_as_bytes(file_path)
    r = requests.put(f"{url}{file_path.split('/')[-1]}", data=file_bytes)
    if r.ok:
        return True
    else:
        raise(f"Upload file {file_path} to s3 error")


if __name__ == "__main__":
    file_link = "http://minio:9000/videos/test.mp4"
    file_path = download_file(file_link)
    print("File downloaded", file_path)

    print("Upload file to s3")
    file_path = "output/test.mp4"
    upload_file(file_path, url="http://minio:9000/processed-videos/")
    print("File uploaded to s3")
