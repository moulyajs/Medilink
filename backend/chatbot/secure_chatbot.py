from agents.semantic_firewall import SemanticFirewall
from agents.query_sanitizer import QuerySanitizer
from rag.vector_store import VectorStore
from llm.medical_agent import MedicalAgent


class SecureMedicalChatbot:

    def __init__(self):

        self.firewall = SemanticFirewall()

        self.sanitizer = QuerySanitizer()

        self.vector = VectorStore()

        self.llm = MedicalAgent()

    def chat(self, query):

        if self.firewall.detect_attack(query):

            return "⚠️ Prompt injection detected."

        clean_query = self.sanitizer.sanitize(query)

        docs = self.vector.search(clean_query)

        context = "\n".join(docs[0])

        answer = self.llm.generate(clean_query, context)

        return answer