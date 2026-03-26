from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import uuid
from dotenv import load_dotenv
import os
load_dotenv()
client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)
COLLECTION_NAME = "lab_report_chunks"


def insert_chunks(chunks, embeddings):
    points = []

    for chunk, embedding in zip(chunks, embeddings):
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload=chunk
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )