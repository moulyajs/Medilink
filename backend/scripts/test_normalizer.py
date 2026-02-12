# test_normalizer.py

import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

known_tests = []
known_vectors = []


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def normalize_test(name):

    if not name:
        return None

    vec = model.encode(name)

    if not known_vectors:
        known_tests.append(name)
        known_vectors.append(vec)
        return name.title()

    sims = [
        cosine_similarity(vec, v)
        for v in known_vectors
    ]

    best_idx = int(np.argmax(sims))
    best_score = sims[best_idx]

    # similarity threshold
    if best_score > 0.85:
        return known_tests[best_idx]

    known_tests.append(name)
    known_vectors.append(vec)

    return name.title()
