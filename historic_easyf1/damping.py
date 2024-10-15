# pip install boto3
# pip install python-dotenv

import boto3
import os
from dotenv import load_dotenv
load_dotenv()

ACCESS_KEY = os.getenv('ACCESS_KEY')
SECRET_KEY = os.getenv('SECRET_ACCESS_KEY')
REGION = os.getenv('BUCKET_REGION')
BUCKET_NAME = os.getenv('BUCKET_NAME')

s3_client = boto3.client(
        service_name='s3',
        region_name=REGION,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY
    )

response = s3_client.upload_file("temp.json", BUCKET_NAME, "test.json")
