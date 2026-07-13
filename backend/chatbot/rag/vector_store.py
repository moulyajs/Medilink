from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from dotenv import load_dotenv
from qdrant_client.models import MatchAny
import os
from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchText,
    MatchValue
)
load_dotenv()
QDRANT_URL = os.getenv(
    "QDRANT_URL",
    "http://qdrant:6333"
)

client = QdrantClient(url=QDRANT_URL)
COLLECTION_NAME = "lab_report_chunks"

def keyword_search_qdrant(
    patient_id,
    keyword,
    limit=20
):

    points, _ = client.scroll(
        collection_name=COLLECTION_NAME,

        scroll_filter=Filter(
            must=[
                FieldCondition(
                    key="patient_id",
                    match=MatchValue(
                        value=patient_id
                    )
                ),

                FieldCondition(
                    key="text",
                    match=MatchText(
                        text=keyword
                    )
                )
            ]
        ),

        limit=limit,
        with_payload=True
    )

    return points

def get_all_patient_chunks(
    patient_id,
    limit=500
):

    points, _ = client.scroll(
        collection_name=COLLECTION_NAME,

        scroll_filter=Filter(
            must=[
                FieldCondition(
                    key="patient_id",
                    match=MatchValue(
                        value=patient_id
                    )
                )
            ]
        ),

        limit=limit,
        with_payload=True
    )

    return points

def get_lab_chunks(
    patient_id,
    test_name,
    limit=100
):

    points, _ = client.scroll(
        collection_name=COLLECTION_NAME,

        scroll_filter=Filter(
            must=[
                FieldCondition(
                    key="patient_id",
                    match=MatchValue(
                        value=patient_id
                    )
                ),

                FieldCondition(
                    key="metadata.test_name",
                    match=MatchValue(
                        value=test_name
                    )
                )
            ]
        ),

        limit=limit,
        with_payload=True
    )

    return points

def search_qdrant(
    query_embedding,
    patient_id,
    chunk_types=None,
    limit=10
):

    must_conditions = [

        FieldCondition(
            key="patient_id",
            match=MatchValue(
                value=patient_id
            )
        )
    ]

    if chunk_types:

        must_conditions.append(

            FieldCondition(
                key="chunk_type",
                match=MatchAny(
                    any=chunk_types
                )
            )
        )

    results = client.query_points(
        collection_name=COLLECTION_NAME,

        query=query_embedding,

        limit=limit,

        query_filter=Filter(
            must=must_conditions
        )
    )

    return results.points

    return results.points