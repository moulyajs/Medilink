import chromadb
from sentence_transformers import SentenceTransformer


class VectorStore:

    def __init__(self):

        self.client = chromadb.Client()

        self.collection = self.client.get_or_create_collection(
            name="medical_records"
        )

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed(self, text):

        return self.model.encode(text).tolist()

    def add_document(self, doc_id, text):

        embedding = self.embed(text)

        self.collection.add(
            ids=[doc_id],
            documents=[text],
            embeddings=[embedding]
        )

    def search(self, query):

        query_embedding = self.embed(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=5
        )

        return results["documents"]