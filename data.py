import boto3
import os
from dotenv import load_dotenv

load_dotenv()

print(os.environ['AWS_ACCESS_KEY'])
