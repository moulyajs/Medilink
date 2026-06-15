from minio import Minio
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET = os.getenv("MINIO_SECRET_KEY", "minioadmin123")

BUCKET = os.getenv("MINIO_BUCKET", "medilink-docs")

client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS,
    secret_key=MINIO_SECRET,
    secure=False
)

# Create bucket if it doesn't exist
if not client.bucket_exists(BUCKET):
    client.make_bucket(BUCKET)

print(f"Connected to MinIO bucket: {BUCKET}")