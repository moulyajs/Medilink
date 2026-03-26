# chatbot/chat_service.py

sessions = {}


def get_session(session_id: str):
    if session_id not in sessions:
        sessions[session_id] = []
    return sessions[session_id]


def update_session(session_id: str, user_query: str, answer: str):
    sessions[session_id].append({
        "role": "user",
        "content": user_query
    })

    sessions[session_id].append({
        "role": "assistant",
        "content": answer
    })