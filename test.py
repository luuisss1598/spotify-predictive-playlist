from dotenv import find_dotenv, load_dotenv
import uuid
import boto3
import os 

env_path = find_dotenv()
load_dotenv(env_path)

aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_access_key,
    region_name='us-west-1'
)

region: str = s3.meta.region_name

unique_id = uuid.uuid4()
bucket_name = f'run-{unique_id}'

response = s3.create_bucket(
    Bucket=bucket_name,
    CreateBucketConfiguration={
        'LocationConstraint': region
    }
)

print(response)
