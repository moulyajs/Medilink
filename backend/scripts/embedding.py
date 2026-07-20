from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-base-en-v1.5")


def embed_chunks(chunks):
    texts = [
        "Represent this medical record for retrieval: " + c["text"]
        for c in chunks
    ]

    return model.encode(texts).tolist()