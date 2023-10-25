import boto3
import os

from botocore.response import StreamingBody
from dotenv import load_dotenv
from data_exceptions import *

load_dotenv()

bucket_name = 'outfit-insiration-database'


def create_client(create_resource=False):
    try:
        if create_resource:
            client = boto3.resource(
                's3',
                aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
                aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                region_name='eu-north-1'
            )
        else:
            client = boto3.client(
                's3',
                aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
                aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                region_name='eu-north-1'
            )
    except Exception as e:
        raise ConnectionException('Could not connect to S3: ' + str(e))

    return client


def upload_file(path: str, key: str) -> None:

    client = create_client()

    try:
        client.upload_file(Filename=path,
                           Bucket=bucket_name,
                           Key=key)
    except Exception as e:
        raise UploadingException('Could not upload file "{0}": '.format(path) + str(e))


def get_bucket_size():
    client = create_client(create_resource=True)

    try:
        bucket = client.Bucket(bucket_name)
        size_in_bytes = sum([key.size for key in bucket.objects.all()])
        return size_in_bytes / (1024 ** 2)
    except Exception as e:
        raise BucketSizeException('Could not count size:' + str(e))


def upload_files_from_folder(path: str,
                             keys: (list[str] | None) = None,
                             allowed_size_in_mb: int = 4608) -> None:

    bucket_size = get_bucket_size()
    print(bucket_size)

    if bucket_size >= allowed_size_in_mb:
        raise BucketOverflowException('Bucket is full, could not upload files')

    client = create_client()
    files = os.listdir(path)
    if keys and len(files) != len(keys):
        raise FilesKeysExceptions('Number of files does not equal to number of keys')

    for i, file in enumerate(files):
        key = file if not keys else keys[i]
        path_to_file = path + '/' + file
        print(path_to_file)
        bucket_size += os.path.getsize(path_to_file) / (1024 ** 2)
        print(os.path.getsize(path_to_file), bucket_size)
        if bucket_size >= allowed_size_in_mb:
            raise BucketOverflowException('Bucket is full, could not upload the rest of files')
        try:
            client.upload_file(Filename=path_to_file,
                               Bucket=bucket_name,
                               Key=key)
        except Exception as e:
            raise UploadingException('Could not upload file "{0}": '.format(path) + str(e))


def get_file(key: str) -> StreamingBody:
    client = create_client()
    # file = client.meta.client.download_file('mybucket', 'hello.txt', '/tmp/hello.txt')
    try:
        file = client.get_object(Bucket=bucket_name, Key=key)['Body']
    except Exception as e:
        raise GetFileExceptions('Could not get file: ' + str(e))
    return file


def _save_file(key:str, client, path_to_save: str):
    try:
        client.download_file(Bucket=bucket_name, Key=key, Filename=path_to_save)
    except Exception as e:
        raise GetSaveFileExceptions('Could not get file {0}: '.format(key) + str(e))


def get_and_save_files(keys: (str | list[str]), path_to_save: str):
    client = create_client()

    if isinstance(keys, str):
        _save_file(keys, client, path_to_save)
    else:
        for key in keys:
            _save_file(key, client, path_to_save + '/' + key)
