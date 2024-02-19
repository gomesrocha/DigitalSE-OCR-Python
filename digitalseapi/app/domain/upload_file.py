
from minio import Minio
import os
import shutil


def _save_file_to_server(uploaded_file, path=".", save_as="default"):
    temp_file = os.path.join(path, save_as)
    os.makedirs(os.path.dirname(temp_file), exist_ok=True)
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)

    return temp_file



def upload_to_minio(minio_client: Minio, file_path, bucket_name, object_name):
    # Upload file to MinIO
    with open(file_path, 'rb') as file_data:
        minio_client.put_object(bucket_name, object_name, file_data, length=os.stat(file_path).st_size)

