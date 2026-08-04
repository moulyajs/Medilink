def handle_greeting():

    return {
        "type": "greeting",
        "content": (
            "Hello! 👋 I'm Medilink AI. "
            "How can I help you with your medical records today?"
        )
    }


def handle_thanks():

    return {
        "type": "thanks",
        "content": (
            "You're welcome! Feel free to ask about your reports, "
            "lab results, or medical history."
        )
    }


def handle_bye():

    return {
        "type": "bye",
        "content": (
            "Take care! I'm here whenever you need help "
            "with your health records."
        )
    }