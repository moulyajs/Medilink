from sentence_transformers import SentenceTransformer

# Load once
model = SentenceTransformer("BAAI/bge-base-en-v1.5")


def get_embedding(text: str):
    text = "Represent this medical record for retrieval: " + text
    return model.encode(text).tolist()