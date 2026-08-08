# see_chunks.py

from qdrant_client import QdrantClient
from dotenv import load_dotenv
import os
import json

load_dotenv()

QDRANT_URL = os.getenv(
    "QDRANT_URL",
    "http://qdrant:6333"
)

client = QdrantClient(url=QDRANT_URL)

all_points = []
offset = None

while True:
    points, offset = client.scroll(
        collection_name="lab_report_chunks",
        limit=100,          # fetch 100 at a time
        offset=offset,
        with_payload=True,
        with_vectors=False
    )

    all_points.extend(points)

    if offset is None:
        break

print(f"\nTotal Chunks: {len(all_points)}\n")
print("=" * 100)

for i, point in enumerate(all_points, start=1):
    print(f"\nChunk {i}")
    print("-" * 100)
    print(f"Point ID      : {point.id}")
    print(f"Chunk ID      : {point.payload.get('chunk_id')}")
    print(f"Document ID   : {point.payload.get('document_id')}")
    print(f"Patient ID    : {point.payload.get('patient_id')}")
    print(f"Chunk Type    : {point.payload.get('chunk_type')}")
    print(f"Chunk Level   : {point.payload.get('chunk_level')}")
    print(f"Report Date   : {point.payload.get('report_date')}")
    print(f"Report Type   : {point.payload.get('report_type')}")

    print("\nMetadata:")
    print(json.dumps(point.payload.get("metadata", {}), indent=4))

    print("\nText:")
    print(point.payload.get("text"))

print("\nDone.")