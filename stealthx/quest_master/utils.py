import pathlib
import re
from hashlib import md5
from random import randrange

import boto3
from environs import Env

from stealthx.models import QuestBook

env = Env()
env.read_env()


def quest_code_exist(code):
    obj = QuestBook.query.filter_by(code=code).first()

    if obj:
        return True

    return False


def clean_blob(blob_url):
    clean = blob_url.lower()
    clean = clean.replace(" ", "-")

    # Remove Non alphanumeric
    clean = re.sub(r"[^a-zA-Z0-9\-]", "", clean)

    # Remove leading hyphens
    clean = re.sub(r"^[-]|[-]$", "", clean)

    # Check if exists
    while quest_code_exist(clean):
        clean = clean + f"-{randrange(99)}"

    return clean


def s3_upload_image(field):
    # resize image

    file_data = field.data.read()

    extension = pathlib.Path(field.data.filename).suffix
    filename = f"{md5(file_data).hexdigest()}{extension}"

    aws_access = env.str("AWS_S3_ACCESS")
    aws_secret = env.str("AWS_S3_SECRET")
    endpoint = env.str("AWS_S3_ENDPOINT_STATIC")

    client = boto3.client('s3',
                          region_name='us-east-1',
                          endpoint_url=endpoint,
                          aws_access_key_id=aws_access,
                          aws_secret_access_key=aws_secret
                          )

    client.put_object(Body=file_data,
                      Bucket="images",
                      Key=filename,
                      ContentType=field.data.content_type,
                      ACL="public-read")

    return f"{endpoint}/images/{filename}"
