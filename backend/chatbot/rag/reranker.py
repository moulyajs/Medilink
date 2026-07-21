from sentence_transformers import CrossEncoder

# Lightweight but powerful
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank(query, chunks, top_k=5):
    
    pairs = [[query, c["text"]] for c in chunks]

    scores = reranker.predict(pairs)

    scored_chunks = list(zip(chunks, scores))
    ranked = sorted(scored_chunks, key=lambda x: x[1], reverse=True)
    top_chunks = [c[0] for c in ranked[:top_k]]
    print("\n" + "="*80)
    print("FINAL TOP CHUNKS")
    print("="*80)

    for i, chunk in enumerate(
    top_chunks,
    start=1
):

        print(
        f"\n[{i}]"
    )

        print(
        "Date:",
        chunk.get("report_date")
    )

        print(
        "Type:",
        chunk.get("chunk_type")
    )

        print(
        chunk.get("text","")[:250]
    )
    return [c[0] for c in ranked[:top_k]]