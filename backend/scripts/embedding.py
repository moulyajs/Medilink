from sentence_transformers import SentenceTransformer

model = None


def get_model():
    global model

    if model is None:
        model = SentenceTransformer("BAAI/bge-base-en-v1.5")

    return model


def embed_chunks(chunks):
    model = get_model()

    texts = [
        "Represent this sentence for retrieval: " + c["text"]
        for c in chunks
    ]

    return model.encode(texts).tolist()