import os

import boto3
from botocore.exceptions import ClientError
from loguru import logger

S3_BUCKET = os.getenv("S3_BUCKET")

S3 = boto3.client("s3")

async def read_thread_id(user_id: int):
    try:
        response = S3.get_object(Bucket=S3_BUCKET, Key=f"threads/{user_id}")
        thread_id = response["Body"].read().decode("utf-8")
        return thread_id
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchKey":
            return None
    except:
        raise

async def delete_thread_id(user_id: int):
    S3.delete_object(Bucket=S3_BUCKET, Key=f"threads/{user_id}")

async def write_thread_id(user_id: int, thread_id: str):
    S3.put_object(Bucket=S3_BUCKET, Key=f"threads/{user_id}", Body=thread_id.encode("utf-8"))