import sys
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
sys.path.append(BASE_DIR)

from chatbot.rag.pipeline import rag_pipeline

patient_id = "f61c1794-5f1a-4dff-9ae9-9d8bcb367c07"

chat_history = []

print("🧠 Interactive Medical Chatbot (type 'exit' to quit)\n")

while True:

    query = input("You: ")

    if query.lower() == "exit":
        break

    response = rag_pipeline(query, patient_id, chat_history)

    print("\n🤖:", response["answer"], "\n")

    # Update history
    chat_history.append({"role": "user", "content": query})
    chat_history.append({"role": "assistant", "content": response["answer"]})