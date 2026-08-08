from minio import Minio
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

# Read environment variables
MINIO_HOST = os.getenv("MINIO_HOST", "minio:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
BUCKET = os.getenv("MINIO_BUCKET", "health-records")

print("MINIO_HOST =", MINIO_HOST)
print("BUCKET =", BUCKET)

# Create MinIO client
client = Minio(
    MINIO_HOST,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

# Create bucket if it doesn't exist
if not client.bucket_exists(BUCKET):
    client.make_bucket(BUCKET)

print(f"Connected to MinIO bucket: {BUCKET}")