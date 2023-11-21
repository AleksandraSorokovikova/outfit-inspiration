from typing import Union

import boto3  # type: ignore
import os

from botocore.response import StreamingBody  # type: ignore
from dotenv import load_dotenv
from data import data_exceptions
from tqdm import tqdm

load_dotenv()

bucket_name = "outfit-insiration-database"


def create_client(create_resource: bool = False) -> Union[boto3.client, boto3.resource]:
    try:
        if create_resource:
            client = boto3.resource(
                "s3",
                aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
                aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
                region_name="eu-north-1",
            )
        else:
            client = boto3.client(
                "s3",
                aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
                aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
                region_name="eu-north-1",
            )
    except Exception as e:
        raise data_exceptions.ConnectionException("Could not connect to S3: " + str(e))

    return client


def upload_file(path: str, key: str) -> None:
    client = create_client()

    try:
        client.upload_file(Filename=path, Bucket=bucket_name, Key=key)
    except Exception as e:
        raise data_exceptions.UploadingException(
            'Could not upload file "{0}": '.format(path) + str(e)
        )


def get_bucket_size() -> float:
    client = create_client(create_resource=True)

    try:
        bucket = client.Bucket(bucket_name)
        size_in_bytes = sum([key.size for key in bucket.objects.all()])
        return size_in_bytes / (1024**2)
    except Exception as e:
        raise data_exceptions.BucketSizeException("Could not count size:" + str(e))


def upload_files_from_folder(
    path: str, keys: list[str] | None = None, allowed_size_in_mb: int = 4608
) -> None:
    files = os.listdir(path)
    paths_to_files = [f"{path}/{file}" for file in files]
    upload_files(paths=paths_to_files, keys=keys, allowed_size_in_mb=allowed_size_in_mb)


def upload_files(
    paths: list[str], keys: list[str] | None = None, allowed_size_in_mb: int = 4608
) -> None:
    bucket_size = get_bucket_size()

    if bucket_size >= allowed_size_in_mb:
        raise data_exceptions.BucketOverflowException(
            "Bucket is full, could not upload files"
        )

    client = create_client()
    if keys and len(paths) != len(keys):
        raise data_exceptions.FilesKeysExceptions(
            "Number of files does not equal to number of keys"
        )

    for i, file in enumerate(tqdm(paths)):
        key = file if not keys else keys[i]
        bucket_size += os.path.getsize(file) / (1024**2)
        if bucket_size >= allowed_size_in_mb:
            raise data_exceptions.BucketOverflowException(
                "Bucket is full, could not upload the rest of files"
            )
        try:
            client.upload_file(Filename=file, Bucket=bucket_name, Key=key)
        except Exception as e:
            raise data_exceptions.UploadingException(
                'Could not upload file "{0}": '.format(file) + str(e)
            )


def get_file(key: str) -> StreamingBody:
    client = create_client()
    try:
        file = client.get_object(Bucket=bucket_name, Key=key)["Body"]
    except Exception as e:
        raise data_exceptions.GetFileExceptions("Could not get file: " + str(e))
    return file


def _save_file(
    key: str, client: Union[boto3.client, boto3.resource], path_to_save: str
) -> None:
    try:
        client.download_file(Bucket=bucket_name, Key=key, Filename=path_to_save)
    except Exception as e:
        raise data_exceptions.GetSaveFileExceptions(
            "Could not get file {0}: ".format(key) + str(e)
        )


def get_and_save_files(keys: str | list[str], path_to_save: str) -> None:
    client = create_client()

    if isinstance(keys, str):
        _save_file(keys, client, path_to_save)
    else:
        for key in tqdm(keys):
            _save_file(key, client, path_to_save + "/" + key)
