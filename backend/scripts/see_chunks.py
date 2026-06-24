#see_chunks.py
from qdrant_client import QdrantClient

from dotenv import load_dotenv
import os
load_dotenv()
QDRANT_URL = os.getenv(
    "QDRANT_URL",
    "http://qdrant:6333"
)

client = QdrantClient(url=QDRANT_URL)

points = client.scroll("lab_report_chunks")

print(points)

