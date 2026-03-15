from sentence_transformers import SentenceTransformer, util

class PromptInjectionAgent:

    def __init__(self):

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.attack_patterns = [
            "ignore previous instructions",
            "reveal system prompt",
            "bypass security",
            "show database",
            "act as admin",
            "delete records"
        ]

        self.embeddings = self.model.encode(self.attack_patterns)

    def analyze(self, query):

        query_embedding = self.model.encode(query)

        similarity = util.cos_sim(query_embedding, self.embeddings)

        if similarity.max() > 0.7:
            return True

        return False