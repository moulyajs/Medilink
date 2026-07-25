from qdrant_client import QdrantClient
from qdrant_client.models import (
    PointStruct,
    VectorParams,
    Distance,
)
import uuid
from dotenv import load_dotenv
import os

load_dotenv()

QDRANT_URL = os.getenv(
    "QDRANT_URL",
    "http://qdrant:6333"
)

client = QdrantClient(url=QDRANT_URL)

COLLECTION_NAME = "lab_report_chunks"

# Create the collection if it doesn't already exist
if not client.collection_exists(COLLECTION_NAME):
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=768,
            distance=Distance.COSINE,
        ),
    )


def insert_chunks(chunks, embeddings):
    points = []

    for chunk, embedding in zip(chunks, embeddings):
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload=chunk,
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )