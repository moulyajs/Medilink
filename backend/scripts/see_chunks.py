#see_chunks.py
from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")

points = client.scroll("lab_report_chunks")

print(points)

