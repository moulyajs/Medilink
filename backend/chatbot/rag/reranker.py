from sentence_transformers import CrossEncoder

# Lightweight but powerful
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank(query, chunks, top_k=5):
    pairs = [[query, c["text"]] for c in chunks]

    scores = reranker.predict(pairs)

    scored_chunks = list(zip(chunks, scores))
    ranked = sorted(scored_chunks, key=lambda x: x[1], reverse=True)

    return [c[0] for c in ranked[:top_k]]