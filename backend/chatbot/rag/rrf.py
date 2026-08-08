def reciprocal_rank(rank, k=60):
    return 1 / (k + rank)


def rrf_fusion(
    vector_results,
    keyword_results
):

    scores = {}

    # -------------------------
    # Vector Results
    # -------------------------

    for rank, chunk in enumerate(
        vector_results,
        start=1
    ):

        chunk_id = chunk["chunk_id"]

        if chunk_id not in scores:
            scores[chunk_id] = {
                "chunk": chunk,
                "score": 0
            }

        scores[chunk_id]["score"] += (
            reciprocal_rank(rank)
        )

    # -------------------------
    # Keyword Results
    # -------------------------

    for rank, chunk in enumerate(
        keyword_results,
        start=1
    ):

        chunk_id = chunk["chunk_id"]

        if chunk_id not in scores:
            scores[chunk_id] = {
                "chunk": chunk,
                "score": 0
            }

        scores[chunk_id]["score"] += (
            reciprocal_rank(rank)
        )

    return sorted(
        scores.values(),
        key=lambda x: x["score"],
        reverse=True
    )