from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(url="http://localhost:6333")

COLLECTION_NAME = "lab_report_chunks"

client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(
        size=768,
        distance=Distance.COSINE
    )
)

print("✅ Collection created successfully")

client.create_payload_index(
    collection_name=COLLECTION_NAME,
    field_name="patient_id",
    field_schema="keyword"
)

print("✅ patient_id index created successfully")