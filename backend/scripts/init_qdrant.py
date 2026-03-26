from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from dotenv import load_dotenv
import os

load_dotenv()

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

COLLECTION_NAME = "lab_report_chunks"

# 🔥 Step 1: Recreate collection
client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(
        size=768,  # BGE embedding size
        distance=Distance.COSINE
    )
)

print("✅ Collection created successfully")

# 🔥 Step 2: Create payload index (VERY IMPORTANT)
client.create_payload_index(
    collection_name=COLLECTION_NAME,
    field_name="patient_id",
    field_schema="keyword"   # or "uuid"
)

print("✅ patient_id index created successfully")