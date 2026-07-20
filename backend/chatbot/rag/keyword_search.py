import re


def extract_keywords(query):

    query = query.upper()

    words = re.findall(
        r"[A-Z0-9]+",
        query
    )

    stopwords = {
        "WHAT",
        "IS",
        "MY",
        "THE",
        "SHOW",
        "ME",
        "OF",
        "AND",
        "IN"
    }

    return [
        w
        for w in words
        if w not in stopwords
        and len(w) > 2
    ]