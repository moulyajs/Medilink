from secure_chatbot import SecureMedicalChatbot


bot = SecureMedicalChatbot()


while True:

    query = input("Ask medical question: ")

    response = bot.chat(query)

    print("Chatbot:", response)