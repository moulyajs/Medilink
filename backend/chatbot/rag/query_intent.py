"""
def detect_intent(query: str):

    q = query.lower()

    if "latest" in q:
        return "LATEST_LAB"

    if "trend" in q:
        return "LAB_TREND"

    if "history" in q:
        return "LAB_HISTORY"

    if "abnormal" in q:
        return "ABNORMAL_LABS"

    return "GENERAL_RAG"


def extract_lab_name(query: str):

    words = query.upper().split()

    return words
"""
##not being used