import os
from dotenv import load_dotenv
from minio import Minio

# Load .env
load_dotenv()

MINIO_HOST = os.getenv("MINIO_HOST")
MINIO_ACCESS = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET = os.getenv("MINIO_SECRET_KEY")
BUCKET = os.getenv("MINIO_BUCKET")


client = Minio(
    MINIO_HOST,
    access_key=MINIO_ACCESS,
    secret_key=MINIO_SECRET,
    secure=False
)

# Create bucket if not exists
if not client.bucket_exists(BUCKET):
    client.make_bucket(BUCKET)
