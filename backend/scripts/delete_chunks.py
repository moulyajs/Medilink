# delete_chunks.py

from qdrant_client import QdrantClient
from qdrant_client.models import Filter

from dotenv import load_dotenv
import os

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL", "http://qdrant:6333")

client = QdrantClient(url=QDRANT_URL)

client.delete(
    collection_name="lab_report_chunks",
    points_selector=Filter(),   # Empty filter matches all points
    wait=True
)

print("✅ All chunks deleted from lab_report_chunks")