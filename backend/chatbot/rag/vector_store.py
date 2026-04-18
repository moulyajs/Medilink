from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from dotenv import load_dotenv
import os
load_dotenv()

client = QdrantClient(url="http://localhost:6333")
COLLECTION_NAME = "lab_report_chunks"


def search_qdrant(query_embedding, patient_id, limit=10):

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=limit,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="patient_id",
                    match=MatchValue(value=patient_id)
                )
            ]
        )
    )

    return results.points