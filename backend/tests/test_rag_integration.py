
from unittest.mock import Mock

import pytest


# INT-RAG-01: Embedding generation

def test_int_rag_01_embedding_generation(monkeypatch):
    import numpy as np
    from chatbot.rag import embeddings
    from unittest.mock import Mock

    fake_model = Mock()
    fake_model.encode.return_value = np.array([0.1, 0.2, 0.3])
    monkeypatch.setattr(embeddings, "model", fake_model)

    result = embeddings.get_embedding("haemoglobin result")

    assert result == [0.1, 0.2, 0.3]
    fake_model.encode.assert_called_once_with(
        "Represent this medical record for retrieval: haemoglobin result"
    )



# INT-RAG-02: Embeddings and chunk metadata stored together
def test_int_rag_02_vector_storage(monkeypatch):
    from scripts import vector_store

    upsert = Mock()
    monkeypatch.setattr(vector_store.client, "upsert", upsert)

    chunks = [
        {
            "chunk_id": "synthetic-chunk-1",
            "patient_id": "synthetic-patient-1",
            "text": "Synthetic haemoglobin result",
        }
    ]
    vectors = [[0.1, 0.2, 0.3]]

    vector_store.insert_chunks(chunks, vectors)

    upsert.assert_called_once()
    kwargs = upsert.call_args.kwargs
    assert kwargs["collection_name"] == vector_store.COLLECTION_NAME
    assert len(kwargs["points"]) == 1
    assert kwargs["points"][0].vector == vectors[0]
    assert kwargs["points"][0].payload == chunks[0]


# INT-RAG-04: Vector search returns candidate chunks
def test_int_rag_04_vector_search(monkeypatch):
    from chatbot.rag import vector_store

    point = Mock()
    point.payload = {
        "patient_id": "patient-a",
        "chunk_id": "chunk-a",
        "text": "Synthetic lab result",
    }
    point.score = 0.9

    query_points = Mock()
    query_points.return_value.points = [point]
    monkeypatch.setattr(vector_store.client, "query_points", query_points)

    result = vector_store.search_qdrant(
        query_embedding=[0.1, 0.2, 0.3],
        patient_id="patient-a",
        limit=10,
    )

    assert result == [point]
    kwargs = query_points.call_args.kwargs
    assert kwargs["limit"] == 10
    assert kwargs["query"] == [0.1, 0.2, 0.3]


# INT-RAG-06: Hybrid fusion combines vector and keyword results
def test_int_rag_06_hybrid_fusion():
    from chatbot.rag.rrf import rrf_fusion

    vector_results = [
        {"chunk_id": "a", "text": "A"},
        {"chunk_id": "b", "text": "B"},
    ]
    keyword_results = [
        {"chunk_id": "b", "text": "B"},
        {"chunk_id": "c", "text": "C"},
    ]

    result = rrf_fusion(vector_results, keyword_results)

    ids = [item["chunk"]["chunk_id"] for item in result]
    assert ids[0] == "b"
    assert set(ids) == {"a", "b", "c"}


# INT-RAG-07: Reranker orders candidates by score
def test_int_rag_07_reranking(monkeypatch):
    from chatbot.rag import reranker as reranker_module

    fake_cross_encoder = Mock()
    fake_cross_encoder.predict.return_value = [0.1, 0.9, 0.3]
    monkeypatch.setattr(
        reranker_module, "reranker", fake_cross_encoder
    )

    chunks = [
        {"text": "Candidate A"},
        {"text": "Candidate B"},
        {"text": "Candidate C"},
    ]

    result = reranker_module.rerank(
        "synthetic query", chunks, top_k=2
    )

    assert [chunk["text"] for chunk in result] == [
        "Candidate B",
        "Candidate C",
    ]


# INT-RAG-12: Patient filter is included in vector search
def test_int_rag_12_patient_isolation_filter(monkeypatch):
    from chatbot.rag import vector_store

    query_points = Mock()
    query_points.return_value.points = []
    monkeypatch.setattr(vector_store.client, "query_points", query_points)

    vector_store.search_qdrant(
        query_embedding=[0.1, 0.2, 0.3],
        patient_id="patient-a",
        limit=10,
    )

    query_filter = query_points.call_args.kwargs["query_filter"]
    conditions = query_filter.must

    patient_conditions = [
        condition
        for condition in conditions
        if condition.key == "patient_id"
    ]

    assert len(patient_conditions) == 1
    assert patient_conditions[0].match.value == "patient-a"
